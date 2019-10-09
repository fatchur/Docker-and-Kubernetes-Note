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


def reconnect(camera_name):
    """The method to release and recreate new opencv videocapture 
       of the disconnected cameras 
    
    Arguments:
        camera_name {bytes} -- the name of the camera
    """
    cap_dict[camera_name].release()
    cap_dict[camera_name] = cv2.VideoCapture(camera_dict[camera_name].decode("utf-8"))
    print ('===>>> reconnect')


def stream():
    global camera_dict, cap_dict, camera_name_connectionproblem, camera_name_encodeproblem

    while(True):
        # ---------------------------------- #
        # for each 100 counts, refresh the camera dictinary
        # - remove the deleted cameras       #
        # - add the new inserted cameras     #
        # ---------------------------------- #
        old_camera_namelist = list(camera_dict.keys())
        update_camera_dict()
        new_camera_namelist = list(camera_dict.keys())

        deleted_camera = get_deleted_camera(old_camera_namelist, new_camera_namelist)
        for i in deleted_camera: 
            cap_dict[i].release()
            del cap_dict[i]

        new_camera = get_new_camera(old_camera_namelist, new_camera_namelist)
        for i in new_camera: 
            cap_dict[i] = cv2.VideoCapture(camera_dict[i].decode("utf-8"))
        
        #print ('cap dict', cap_dict)
        #print ('camera dict', camera_dict)
        #print ('connection error', camera_name_connectionproblem)
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
            # zmq payload preparation            #
            # check the connection status        #
            # check the encoding process         #
            # ---------------------------------- #
            for name in camera_frame: 
                if camera_frame[name]['ret'] == True: 
                    img = camera_frame[name]['frame']
                    img = cv2.resize(img, (570, 420))
                    jpg_success, img = cv2.imencode('.jpg', img)

                    if jpg_success:
                        transferred_data[name.decode("utf-8")] = base64.b64encode(img).decode()
                    else: 
                        transferred_data[name.decode("utf-8")] = None
                        camera_name_encodeproblem.append(name.decode("utf-8"))

                else: 
                    transferred_data[name.decode("utf-8")] = None
                    if name not in camera_name_connectionproblem: 
                        camera_name_connectionproblem.append(name.decode("utf-8"))
                        reconnect(name)

            # ---------------------------------- #
            # transmit data via kafka            #
            # ---------------------------------- #
            producer.send('ai_topic', value=transferred_data)
            time.sleep(0.05)


if __name__ == '__main__':
    stream()






