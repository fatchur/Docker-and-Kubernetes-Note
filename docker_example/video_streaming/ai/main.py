import io
import cv2 
import json
import base64
import logging
import numpy as np
from PIL import Image
import tensorflow as tf
from kafka import KafkaConsumer
from kafka import KafkaProducer
from simple_tensor.object_detector.yolo import Yolo 


def stringToImage(base64_string):
    """Function for decoding the base64 image
    
    Arguments:
        base64_string {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    imgData = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgData)) 


# ---------------------------------- #
# logging setup                      #
# ---------------------------------- #
logging.basicConfig(filename='/home/ai.log', 
                    filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('======= SYSTEM WARMINGUP =========')

# ---------------------------------- #
# initializing yolo object           #
# building yolo network              #
# restoring model                    #
# ---------------------------------- #
simple_yolo = Yolo(num_of_class=4,
         objectness_loss_alpha=10., 
         noobjectness_loss_alpha=0.1, 
         center_loss_alpha=10., 
         size_loss_alpha=10., 
         class_loss_alpha=10.,
         add_modsig_toshape=True,
         dropout_rate = 0.2) 

simple_yolo.build_net(input_tensor=c.input_placeholder, is_training=False, network_type='very_small') 
saver_all = tf.train.Saver()
session = tf.Session()
session.run(tf.global_variables_initializer())
saver_all.restore(session, '/home/models/yolov3')
logging.warning('===>>> INFO: Load model success ...')

# ---------------------------------- #
# setting kafka consumer             #
# ---------------------------------- #
consumer = KafkaConsumer('ai_topic',
                        bootstrap_servers=['0.0.0.0:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='ai-group',
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
logging.warning('===>>> INFO: Kafka consumer ON ...')

# ---------------------------------- #
# initializing kafka producer        #
# ---------------------------------- #
producer = KafkaProducer(bootstrap_servers=['0.0.0.0:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))
logging.warning('===>>> INFO: Kafka producer ON ...')

# ---------------------------------- #
# get the string image from kafka    #
# input preprocessing                #
# ---------------------------------- #
for message in consumer:
    message = message.value
    
    images = []
    images_b64 = []
    ids = []
    statuses = []
    for i in(message):
        frame = message[i]['b64']
        status =  message[i]['success']
        img = stringToImage(frame)
        img = cv2.resize(img, (416, 416)).astype(np.float32)
        img = img / 255. 
        images.append(img)
        images_b64.append(frame)
        ids.append(i)
        statuses.append(status)
    
    batch = len(images)
    images = np.array(images)
    images = images.reshape((batch, 416, 416, 3))

    # ---------------------------------- #
    # inference                          #
    # ---------------------------------- #
    detection_result = session.run(simple_yolo.boxes_dicts, feed_dict={simple_yolo.input_placeholder: images})
    bboxes = simple_yolo.nms(detection_result, 0.8, 0.1) #[[x1, y1, w, h], [...]]

    # ---------------------------------- #
    # transmit data via kafka            #
    # ---------------------------------- #
    transferred_data = {}
    for idx, i in enumerate(ids): 
        transferred_data[i] = {}
        transferred_data[i]["frame"] = images_b64[idx]
        transferred_data[i]["status"] = statuses[idx]
        transferred_data[i]["bboxes"] = bboxes[idx]

    producer.send('visualizer_topic', value=transferred_data)



            


