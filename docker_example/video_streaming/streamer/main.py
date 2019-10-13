import cv2 
import time
import redis 
import pickle
import base64
import numpy as np 
from json import dumps
from kafka import KafkaProducer


# ---------------------------------- #
# initializing kafka producer        #
# ---------------------------------- #
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))
# ---------------------------------- #
# initializing the redis db          #
# ---------------------------------- #
r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8")
# ---------------------------------- #
# initializing global variables      #
# ---------------------------------- #
camera_dict = {}
cap_dict = {}
camera_name_connectionproblem = []
camera_name_encodeproblem  = []

IMG_INVALID_URL = cv2.imread('assets/invalid_url200.jpg')
IMG_CONNECTION_ERROR = cv2.imread('assets/connection_error200.jpg')
IMG_ENCODE_ERROR = cv2.imread('assets/encode_error200.jpg')
IMG_INVALID_URL = cv2.imencode('.jpg', IMG_INVALID_URL)[1]
IMG_CONNECTION_ERROR = cv2.imencode('.jpg', IMG_CONNECTION_ERROR)[1]
IMG_ENCODE_ERROR = cv2.imencode('.jpg', IMG_ENCODE_ERROR)[1]


def update_camera_dict():
    """Functioin for update the camera url from redis
    """
    global camera_dict
    camera_dict = r.hgetall("video_dict")


def get_deleted_camera(old_camera_namelist, 
                       new_camera_namelist):
    """Function for getting the deleted camera names
    
    Arguments:
        old_camera_namelist {list of str} -- the list of previous camera names
        new_camera_namelist {list od str} -- the list of new camera names
    
    Returns:
        [list of str] -- the list of deleted camera names 
    """
    deleted = [x for x in old_camera_namelist if x not in new_camera_namelist]
    return deleted


def get_new_camera(old_camera_namelist, 
                   new_camera_namelist):
    """Function for getting the new camera names
    
    Arguments:
        old_camera_namelist {list of str} -- the list of previous camera names
        new_camera_namelist {list od str} -- the list of new camera names
    
    Returns:
        [list of str] -- the list of new camera names 
    """
    new_camera = [x for x in new_camera_namelist if x not in old_camera_namelist]
    return new_camera


def get_edited_camera(old_camera_dict):
    """Function for getting the edited camera
    
    Arguments:
        old_camera_dict {[type]} -- [description]
    """
    edited = []
    for i in old_camera_dict: 
        old_url = old_camera_dict[i]
        # ---------------------------------- #
        # TRY if the camera name was not deleted
        # ---------------------------------- #
        try:
            new_url = camera_dict[i]
            if old_url != new_url: 
                edited.append(i)
        except: 
            pass 


def reconnect(camera_name):
    """The method to release and recreate new opencv videocapture 
       of the disconnected cameras 
    
    Arguments:
        camera_name {bytes} -- the name of the camera
    """
    global camera_dict, cap_dict

    try:
        cap_dict[camera_name].release()
        cap_dict[camera_name] = cv2.VideoCapture(camera_dict[camera_name].decode("utf-8"))
    except: 
        pass


def stream():
    global camera_dict, cap_dict, camera_name_connectionproblem, camera_name_encodeproblem

    while(True):
        # ---------------------------------- #
        # for each 10 counts, refresh the camera and cap dictionary
        # - remove the deleted cameras       #
        # - add the new inserted cameras     #
        # - update the edited camera url     #
        # ---------------------------------- #
        old_camera_namelist = list(camera_dict.keys())
        old_camera_dict = camera_dict.copy()
        update_camera_dict()
        new_camera_namelist = list(camera_dict.keys())

        deleted_camera = get_deleted_camera(old_camera_namelist, new_camera_namelist)
        for i in deleted_camera: 
            cap_dict[i].release()
            del cap_dict[i]

        new_camera = get_new_camera(old_camera_namelist, new_camera_namelist)
        for i in new_camera: 
            cap_dict[i] = cv2.VideoCapture(camera_dict[i].decode("utf-8"))

        edited_camera = get_edited_camera(old_camera_dict)
        for i in edited_camera: 
            cap_dict[i].release()
            cap_dict[i] = cv2.VideoCapture(camera_dict[i].decode("utf-8"))

        # ---------------------------------- #
        # list for capturing the:            #
        # connection and encoding problems   #
        # for each 10 iterations             #
        # ---------------------------------- #
        camera_name_connectionproblem = []
        camera_name_encodeproblem = []

        for i in range(10):
            transferred_data = {}
            camera_frame = {}
            
            # ---------------------------------- #
            # get the connection status (connect or not)
            # get the image frame                #
            # store it in camera_frame dictionary#
            # ---------------------------------- #
            for name in cap_dict:
                camera_frame[name] = {}
                camera_frame[name]['ret'], camera_frame[name]['frame'] = cap_dict[name].read()

            # ---------------------------------- #
            # kafka payload preparation            #
            # check the connection status        #
            # check the encoding process         #
            # ---------------------------------- #
            for name in camera_frame: 
                if camera_frame[name]['ret'] == True: 
                    img = camera_frame[name]['frame']
                    img = cv2.resize(img, (200, 200))
                    jpg_success, img = cv2.imencode('.jpg', img)

                    if jpg_success:
                        transferred_data[name.decode("utf-8")] = base64.b64encode(img).decode()
                    else: 
                        transferred_data[name.decode("utf-8")] = base64.b64encode(IMG_ENCODE_ERROR).decode()
                        camera_name_encodeproblem.append(name)

                else: 
                    transferred_data[name.decode("utf-8")] = base64.b64encode(IMG_CONNECTION_ERROR).decode()
                    if name not in camera_name_connectionproblem: 
                        camera_name_connectionproblem.append(name)

            # ---------------------------------- #
            # transmit data via kafka            #
            # ---------------------------------- #
            producer.send('ai_topic', value=transferred_data)
            time.sleep(0.05)
        
        # ---------------------------------- #
        # reconnect the camera               #
        # ---------------------------------- #
        for i in camera_name_connectionproblem:        
            reconnect(i)


if __name__ == '__main__':
    stream()






