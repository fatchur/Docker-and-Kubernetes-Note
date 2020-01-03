import io
import cv2 
import json
import time
import uuid
import redis
import random
import base64
import logging
import datetime
import numpy as np
from PIL import Image
from kafka import KafkaConsumer
import pymysql.cursors



JACKET_CLASS = ["_", "VIOLATION"]
HELM_CLASS = ["_", "VIOLATION"]

# ---------------------------------- #
# logging setup                      #
# ---------------------------------- #
logging.basicConfig(filename='/home/saver.log', 
                    filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('======= SYSTEM WARMINGUP =========')
# ---------------------------------- #
# initializing the redis db          #
# ---------------------------------- #
r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8")
# ---------------------------------- #
# mysql object                       #
# ---------------------------------- #
connection = pymysql.connect(host='0.0.0.0',
                             user='root',
                             password='balongan',
                             db='safety',
                             charset= 'utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit= True)
# ---------------------------------- #
# setting kafka consumer             #
# ---------------------------------- #
consumer = KafkaConsumer('cloud_handler_topic',
                        bootstrap_servers=['0.0.0.0:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='my-group',
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))


def insert_data(id, helm_violation, jacket_violation, data_time): 
    try:
        with connection.cursor() as cursor:
            # Create a new record
            tuple_data = (id, helm_violation, jacket_violation, data_time)
            sql = "INSERT INTO apd_new2 (id, helm_violation, jacket_violation, time) VALUES {}".format(tuple_data)
            cursor.execute(sql)
            cursor.close()

    except Exception as e:
        logging.warning(str(e))


def stringToImage(base64_string):
    """Function for decoding the base64 image
    
    Arguments:
        base64_string {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    imgData = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgData)) 


def initialize_redis_data(): 
    try: 
        with open('ai_setup.json') as json_file:
            data = json.load(json_file)
            r.hmset("ai_setup", data)

        with open('point_dict.json') as json_file:
            data = json.load(json_file)
            tmp = {}
            for i in data: 
                tmp[i] = json.dumps(data[i])
            r.hmset("point_dict", tmp)

        with open('video_dict.json') as json_file:
            data = json.load(json_file)
            tmp = {}
            for i in data: 
                tmp[i] = json.dumps(data[i])
            r.hmset("video_dict", tmp)
        r.set('video_on', 0)

    except Exception as e: 
        logging.warning("Fail to reinitialize redis parameter " + str(e) )


def log_redis_parameter():
    try: 
        ai_setup = r.hgetall("ai_setup")
        tmp_ai = {}
        tmp_ai['bbox_threshold'] = ai_setup['bbox_threshold'.encode("utf-8")].decode("utf-8")
        tmp_ai['class_threshold'] = ai_setup['class_threshold'.encode("utf-8")].decode("utf-8")
        tmp_ai['fps'] = ai_setup['fps'.encode("utf-8")].decode("utf-8")  
        with open('ai_setup.json', 'w') as outfile:
            json.dump(tmp_ai, outfile)

        camera_setup = r.hgetall("video_dict") 
        tmp_cam = {}
        for i in camera_setup: 
            tmp_cam[i.decode("utf8")] = json.loads(camera_setup[i].decode("utf-8")) 
        with open('video_dict.json', 'w') as outfile:
            json.dump(tmp_cam, outfile)

        camera_point = r.hgetall("point_dict") 
        tmp_point = {} 
        for i in camera_point: 
            tmp_point[i.decode("utf8")] = json.loads(camera_point[i].decode("utf-8")) 
        with open('point_dict.json', 'w') as outfile:
            json.dump(tmp_point, outfile)
    
    except Exception as e: 
        logging.warning("Fail to log redis parameter as json file " + str(e))
    

def main():
    """
    Method for setting the video status 'video_on' on redis to zero,
       Called when the first user open a homepage for the first time
    """
    initialize_redis_data()

    # ---------------------------------- #
    # get the string image from kafka    #
    # input preprocessing                #
    # ---------------------------------- #
    for message in consumer:
        if random.randint(0, 10) == 0:
            log_redis_parameter()
        message = message.value

        for i in message: 
            frame = message[i]['b64']
            j_violation = message[i]['j_violation']
            h_violation = message[i]['h_violation']
            bboxes = message[i]['bboxes']

            img = stringToImage(frame)
            img = np.array(img).astype(np.uint8)
            cropped_img = img[bboxes[1]:bboxes[3], bboxes[0]:bboxes[2]]

            # ---------------------------------- #
            # save image                         #
            # ---------------------------------- # 
            img_id = str(uuid.uuid1())
            img_time = str((datetime.datetime.now() + datetime.timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S"))
            img_name = img_time + "_" + img_id + "_" + JACKET_CLASS[j_violation] + "_" + HELM_CLASS[h_violation]
            cv2.imwrite("res/full/" + img_name + "_full.jpg", img)
            cv2.imwrite("res/cropped/" + img_name + "_cropped.jpg", cropped_img)
            cv2.waitKey(33)
            
            # ---------------------------------- #
            # insert to db                       #
            # ---------------------------------- # 
            insert_data(id=img_id, helm_violation=HELM_CLASS[h_violation], jacket_violation=JACKET_CLASS[j_violation], data_time=img_time)
            time.sleep(0.01)


if __name__ == "__main__":
    main()