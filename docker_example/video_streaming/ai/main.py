import io
import cv2 
import json
import base64
import logging
import numpy as np 
from PIL import Image
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

simple_yolo.build_net(input_tensor=c.input_placeholder, is_training=False, network_type='small') 
saver_all = tf.train.Saver()
session = tf.Session()
session.run(tf.global_variables_initializer())
saver_all.restore(session, 'models/yolov3')

# ---------------------------------- #
# setting kafka consumer             #
# ---------------------------------- #
consumer = KafkaConsumer('ai_topic',
                        bootstrap_servers=['0.0.0.0:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='ai-group',
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# ---------------------------------- #
# initializing kafka producer        #
# ---------------------------------- #
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

# ---------------------------------- #
# get the string image from kafka    #
# input preprocessing                #
# ---------------------------------- #
for message in consumer:
    message = message.value
    
    images = []
    ids = []
    statuses = []
    for i in(message):
        frame = message[i]
        img = stringToImage(base64_string)
        img = cv2.resize(img, (416, 416))
        img = img / 255. 
        images.append(img)
        ids.append(i)
        statuses.append('x')
    
    batch = len(images)
    images = np.array(images).astype(np.float32)
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
        transferred_data[i]["frame"] = None
        transferred_data[i]["status"] = statuses[idx]
        
    producer.send('visualizer_topic', value=transferred_data)



            


