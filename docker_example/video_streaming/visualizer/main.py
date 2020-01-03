import io
import cv2 
import json
import time
import redis
import base64
import logging
import numpy as np
from PIL import Image
from kafka import KafkaConsumer
from kafka import KafkaProducer
from comdutils.vis_utils import *
from comdutils.math_utils import *


COLORS = np.random.uniform(0, 255, 255)
TH = 0.472


def stringToImage(base64_string):
    """Function for decoding the base64 image
    
    Arguments:
        base64_string {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    imgData = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgData)) 


def prepare_image(image, cross_bounding_boxes, line_points):
    # ---------------------------------- #
    # draw rectangle                     #
    # draw inspector line                #
    # draw overlay                       #
    # ---------------------------------- #
    image = draw_rectangles(image, cross_bounding_boxes, COLORS)
    cv2.line( image, (line_points[0], line_points[1]), (line_points[2], line_points[3]), (0, 110, 220),  3)
    overlay_bboxs = []
    if len(cross_bounding_boxes) > 0:
        image, overlay_bboxs = put_topoverlays(image, cross_bounding_boxes,)
    return image, overlay_bboxs


def inside_bbox(bbox, center_point): 
    """[summary]
    
    Arguments:
        bbox {[type]} -- [description]
        center_point {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    ctr_x = center_point[0]
    ctr_y = center_point[1]

    bool_x = ctr_x >= bbox[0] and ctr_x <= bbox[2]
    bool_y = ctr_y >= bbox[1] and ctr_y <= bbox[3]

    return bool_x and bool_y


# ---------------------------------- #
# logging setup                      #
# ---------------------------------- #
logging.basicConfig(filename='/home/visualizer.log', 
                    filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('======= SYSTEM WARMINGUP ======')
# ---------------------------------- #
# initializing the redis db          #
# ---------------------------------- #
r = redis.Redis(host='0.0.0.0', port=6379, db=0, charset="utf-8")
# ---------------------------------- #
# setting kafka consumer             #
# ---------------------------------- #
consumer = KafkaConsumer('visualizer_topic',
                        bootstrap_servers=['0.0.0.0:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='visualizer',
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
logging.warning('=> INFO: Kafka consumer ON ...')
# ---------------------------------- #
# initializing kafka producer        #
# ---------------------------------- #
producer = KafkaProducer(bootstrap_servers=['0.0.0.0:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                         batch_size = 0,
                         linger_ms=10)
logging.warning('=> INFO: Kafka producer ON ...')

# ---------------------------------- #
# get the string image from kafka    #
# input preprocessing                #
# ---------------------------------- #
for message in consumer:
    transferred_data = {}
    message = message.value

    for i in(message):
        try: 
            # ---------------------------------- #
            # get the b64 image from kafka       #
            # get the success status from kafka  #
            # get the bboxes from kafka          #
            # ---------------------------------- #
            frame = message[i]['b64']
            status =  message[i]['success']
            bboxes = np.array(message[i]['bboxes'])
            video_name = message[i]['video_name']

            img = stringToImage(frame)
            img = np.array(img).astype(np.uint8)
            
            # ---------------------------------- #
            # get the line point from redis      #
            # ---------------------------------- #
            point_dict = r.hgetall("point_dict")
            json_data = json.loads(point_dict[i.encode("utf-8")].decode("utf-8"))
            y1 = int(json_data['y1'])
            y2 = int(json_data['y2'])
            line = [0,y1, 416, y2]
            
            # ---------------------------------- #
            # select the bbox is person or head  #
            # ---------------------------------- #
            bbox_person = []
            class_person = []
            prob_person = []
            bbox_head = []
            class_head = []
            prob_head = []
            for item in bboxes: 
                tmp_bbox = [int(item[0]), int(item[1]), int(item[0] + item[2]), int(item[1] + item[3])]
                tmp_class = int(item[5])
                tmp_prob = item[6]
                # if tmp_class is 2 or 3 => head
                if tmp_class >= 2:
                    bbox_head.append(tmp_bbox)
                    class_head.append(tmp_class)
                    prob_head.append(tmp_prob)
                else: 
                    bbox_person.append(tmp_bbox)
                    class_person.append(tmp_class)
                    prob_person.append(tmp_prob)

            # ---------------------------------- #
            # check the head bbox belong to wich person  
            # ---------------------------------- #
            object_dict = {}
            for idx, j in enumerate(bbox_person): 
                object_dict[idx] = {}

                for idy, k in enumerate(bbox_head): 
                    x_center = int((k[0] + k[2])/2)
                    y_center = int((k[1] + k[3])/2)
                    is_inside = inside_bbox(j, [x_center, y_center])

                    if is_inside:
                        object_dict[idx]['head_bbox'] = k
                        object_dict[idx]['head_class'] = class_head[idy]
                        object_dict[idx]['head_prob'] = prob_head[idy]
                        break
                
                object_dict[idx]['person_bbox'] = j 
                object_dict[idx]['person_class'] = class_person[idx]
                object_dict[idx]['person_prob'] = prob_person[idx]

            # ---------------------------------- #
            # get the crossing bboxes list       #
            # get the violation list             # 
            # ---------------------------------- #
            cross_bbox = {}
            cross_bbox_list = []
            violation_list = []

            # ---------------------------------- #
            # prepare data to cloud handler topic#
            # ---------------------------------- #
            violation_data = {}

            for j in object_dict: 
                line_inspector = LineInspect(image_shape=img.shape, lines=[line])
                
                if len(line_inspector.is_crossing_line([object_dict[j]['person_bbox']], 0)) != 0:
                    cross_bbox_list.append(object_dict[j]['person_bbox'])

                    # ---------------------------------- #
                    # get the violation labels           #
                    # if condition: head miss detection  #
                    # ---------------------------------- #
                    if 'head_class' in object_dict[j]: 
                        if object_dict[j]['person_class'] == 1 and object_dict[j]['head_class'] == 3: 
                            if object_dict[j]['person_prob'] >= TH and object_dict[j]['head_prob'] >= TH: 
                                violation_data[j] = {}
                                violation_data[j]['b64'] = frame
                                violation_data[j]['j_violation'] = 1
                                violation_data[j]['h_violation'] = 1
                                violation_data[j]['bboxes'] = object_dict[j]['person_bbox']
                                violation_list.append(['VIOLATION'])

                            elif object_dict[j]['person_prob'] >= TH: 
                                violation_data[j] = {}
                                violation_data[j]['b64'] = frame
                                violation_data[j]['j_violation'] = 1
                                violation_data[j]['h_violation'] = 0
                                violation_data[j]['bboxes'] = object_dict[j]['person_bbox']
                                violation_list.append(['VIOLATION'])

                            elif object_dict[j]['head_prob'] >= TH: 
                                violation_data[j] = {}
                                violation_data[j]['b64'] = frame
                                violation_data[j]['j_violation'] = 0
                                violation_data[j]['h_violation'] = 1
                                violation_data[j]['bboxes'] = object_dict[j]['person_bbox']
                                violation_list.append(['VIOLATION'])
                            else: 
                                violation_list.append(['-'])

                        elif object_dict[j]['person_class'] == 1: 
                            if object_dict[j]['person_prob'] >= TH:
                                violation_data[j] = {}
                                violation_data[j]['b64'] = frame
                                violation_data[j]['j_violation'] = 1
                                violation_data[j]['h_violation'] = 0
                                violation_data[j]['bboxes'] = object_dict[j]['person_bbox']
                                violation_list.append(['VIOLATION'])
                                logging.warning('VIOLATION DETECTED J ' + str(object_dict[j]['person_prob']) )
                            else: 
                                violation_list.append(['-'])

                        elif object_dict[j]['head_class'] == 3: 
                            if object_dict[j]['head_prob'] >= TH: 
                                violation_data[j] = {}
                                violation_data[j]['b64'] = frame
                                violation_data[j]['j_violation'] = 0
                                violation_data[j]['h_violation'] = 1
                                violation_data[j]['bboxes'] = object_dict[j]['person_bbox']
                                violation_list.append(['VIOLATION'])
                                logging.warning('VIOLATION DETECTED H ' + str(object_dict[j]['head_prob']) )
                            else: 
                                violation_list.append(['-'])

                        else: 
                            violation_list.append(['OK'])

                    else: 
                        if object_dict[j]['person_class'] == 1: 
                            if object_dict[j]['person_prob'] >= TH:
                                violation_data[j] = {}
                                violation_data[j]['b64'] = frame
                                violation_data[j]['j_violation'] = 1
                                violation_data[j]['h_violation'] = 0
                                violation_data[j]['bboxes'] = object_dict[j]['person_bbox']
                                violation_list.append(['VIOLATION'])
                                logging.warning('VIOLATION DETECTED J--s ' + str(object_dict[j]['person_prob']) )
                            else: 
                                violation_list.append(['-'])

                        else: 
                            violation_list.append(['OK'])
                    
            producer.send('cloud_handler_topic', value=violation_data)  
            producer.flush()
            time.sleep(0.001)

            # ---------------------------------- #
            # visualize the crossing bbox        #
            # put the violation text over head   # 
            # ---------------------------------- #
            img, overlay_bboxs = prepare_image(img, cross_bbox_list, line)
            img = put_vertical_textsoverrect(img, overlay_bboxs, violation_list)
            img = cv2.imencode('.jpg', img)[1]
            img = base64.b64encode(img).decode()

            transferred_data[i] = {}
            transferred_data[i]['b64'] = img
            transferred_data[i]['success'] = status
            transferred_data[i]['video_name'] = video_name

        except Exception as e: 
            logging.warning(e)
    
    producer.send('broadcaster_topic', value=transferred_data)  
    producer.flush()
    time.sleep(0.001)


        



