import cv2 
import time
import json
import redis 
import base64
import logging
import numpy as np 
from json import dumps
from kafka import KafkaProducer


# ---------------------------------- #
# python logging setup               #
# ---------------------------------- #
logging.basicConfig(filename='/home/pertamina.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('======= SYSTEM WARMINGUP =========')
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
    for i in camera_dict: 
        camera_dict[i] = json.loads(camera_dict[i].decode("utf-8"))


def get_deleted_camera(old_camera_idlist, 
                       new_camera_idlist):
    """Function for getting the deleted camera names
    
    Arguments:
        old_camera_namelist {list of str} -- the list of previous camera names
        new_camera_namelist {list od str} -- the list of new camera names
    
    Returns:
        [list of str] -- the list of deleted camera names 
    """
    deleted = [x for x in old_camera_idlist if x not in new_camera_idlist]
    return deleted


def get_new_camera(old_camera_idlist, 
                   new_camera_idlist):
    """Function for getting the new camera names
    
    Arguments:
        old_camera_namelist {list of str} -- the list of previous camera names
        new_camera_namelist {list od str} -- the list of new camera names
    
    Returns:
        [list of str] -- the list of new camera names 
    """
    new_camera = [x for x in new_camera_idlist if x not in old_camera_idlist]
    return new_camera


def get_edited_camera(old_camera_dict):
    """Function for getting the edited camera
    
    Arguments:
        old_camera_dict {[type]} -- [description]
    """
    edited = []
    for i in old_camera_dict: 
        old_url = old_camera_dict[i]['video_url']
        # ---------------------------------- #
        # TRY if the camera name was not deleted
        # ---------------------------------- #
        try:
            new_url = camera_dict[i]['video_url']
            if old_url != new_url: 
                edited.append(i)
        except: 
            pass 
    return edited


def reconnect(cam_id):
    """The method to release and recreate new opencv videocapture 
       of the disconnected cameras 
    
    Arguments:
        camera_name {bytes} -- the name of the camera
    """
    global camera_dict, cap_dict

    try:
        cap_dict[cam_id].release()
        cap_dict[cam_id] = cv2.VideoCapture(camera_dict[cam_id]['video_url'])
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
        old_camera_idlist = list(camera_dict.keys())
        old_camera_dict = camera_dict.copy()
        update_camera_dict()
        new_camera_idlist = list(camera_dict.keys())

        deleted_camera = get_deleted_camera(old_camera_idlist, new_camera_idlist)
        for i in deleted_camera: 
            cap_dict[i].release()
            del cap_dict[i]

        new_camera = get_new_camera(old_camera_idlist, new_camera_idlist)
        for i in new_camera: 
            cap_dict[i] = cv2.VideoCapture(camera_dict[i]['video_url'])

        edited_camera = get_edited_camera(old_camera_dict)
        for i in edited_camera: 
            cap_dict[i].release()
            cap_dict[i] = cv2.VideoCapture(camera_dict[i]['video_url'])
        
        # ---------------------------------- #
        # log for camera changing            #
        # ---------------------------------- #
        if len(deleted_camera) > 0:
            logging.warning("========= old cam: ", str(deleted_camera))
            logging.warning(camera_dict)
        if len(new_camera) > 0:
            logging.warning("========= new cam: " + str(new_camera))
            logging.warning(camera_dict)
        if len(edited_camera) > 0:
            logging.warning("========= edited cam: " + str(edited_camera))
            logging.warning(camera_dict)
        

        # ---------------------------------- #
        # list for capturing the:            #
        # connection and encoding problems   #
        # for each 10 iterations             #
        # ---------------------------------- #
        camera_id_connectionproblem = []
        camera_id_encodeproblem = []

        for i in range(10):
            transferred_data = {}
            camera_frame = {}
            
            # ---------------------------------- #
            # get the connection status (connect or not)
            # get the image frame                #
            # store it in camera_frame dictionary#
            # ---------------------------------- #
            for cam_id in cap_dict:
                camera_frame[cam_id] = {}
                camera_frame[cam_id]['ret'], camera_frame[cam_id]['frame'] = cap_dict[cam_id].read()

            # ---------------------------------- #
            # kafka payload preparation          #
            # check the connection status        #
            # check the encoding process         #
            # ---------------------------------- #
            for cam_id in camera_frame: 
                if camera_frame[cam_id]['ret'] == True: 
                    img = camera_frame[cam_id]['frame']
                    img = cv2.resize(img, (200, 200))
                    jpg_success, img = cv2.imencode('.jpg', img)

                    if jpg_success:
                        transferred_data[cam_id.decode("utf-8")] = {}
                        transferred_data[cam_id.decode("utf-8")]["b64"] = base64.b64encode(img).decode()
                        transferred_data[cam_id.decode("utf-8")]["success"] = True
                    else: 
                        transferred_data[cam_id.decode("utf-8")] = {}
                        transferred_data[cam_id.decode("utf-8")]["b64"] = base64.b64encode(IMG_ENCODE_ERROR).decode()
                        transferred_data[cam_id.decode("utf-8")]["success"] = False
                        camera_name_encodeproblem.append(cam_id)

                else: 
                    transferred_data[cam_id.decode("utf-8")] = {}
                    transferred_data[cam_id.decode("utf-8")]["b64"] = base64.b64encode(IMG_CONNECTION_ERROR).decode()
                    transferred_data[cam_id.decode("utf-8")]["success"] = False
                    if cam_id not in camera_id_connectionproblem: 
                        camera_id_connectionproblem.append(cam_id)

            # ---------------------------------- #
            # transmit data via kafka            #
            # ---------------------------------- #
            producer.send('ai_topic', value=transferred_data)
            time.sleep(0.07)
        
        # ---------------------------------- #
        # reconnect the camera               #
        # ---------------------------------- #
        for i in camera_id_connectionproblem:        
            reconnect(i)


if __name__ == '__main__':
    stream()






