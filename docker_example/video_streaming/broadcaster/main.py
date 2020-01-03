import cv2
import uuid
import time
import json
import redis
import base64
import datetime
import requests
import logging
from kafka import KafkaConsumer
from flask import Flask, request, render_template
from flask_socketio import SocketIO
from flask_cors import CORS


# ---------------------------------- #
# setting kafka consumer             #
# ---------------------------------- #
consumer = KafkaConsumer('broadcaster_topic',
                        bootstrap_servers=['0.0.0.0:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='my-group',
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
# ---------------------------------- #
# 1. initializing the redis db       #
# 2. initializing flask, flask-socketio
# ---------------------------------- #
r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8")
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
# ---------------------------------- #
# logging setup                      #
# ---------------------------------- #
logging.basicConfig(filename='/home/broadcaster.log', filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('======= SYSTEM WARMINGUP =========')


@app.before_first_request
def before_first_request_func():
    """Method for setting the video status 'video_on' on redis to zero,
       Called when the first user open a homepage for the first time
    """
    video_cond = r.get('video_on')
    # ---------------------------------- #
    # The first request of the first user#
    # Set the 'video_on' to zero         #
    # so when the user socket connected, #
    # the streaming will begin           #
    # ---------------------------------- #
    if video_cond is not None: 
        video_cond = int(video_cond)
    elif video_cond==None or video_cond==1:
        r.set('video_on', 0)

    video_cond = r.get('video_on')
    tm = datetime.datetime.now()
    tm = tm.strftime("%c")
    logging.warning("===>>> B. The data of 'video_on' in redis \
                     was reinitialized: " + tm)


@app.route('/web')
def web():
    """ Endpoint for rendering the homepage html
    
    Returns:
        [hmtl] -- html webpage
    """
    return render_template('index.html')


@app.route('/edit_ai', methods=['PUT'])
def edit_ai():
    """Method for adding camera url
    
    Returns:
        [type] -- [description]
    """
    logging.warning("====>>: EDIT AI")
    # ---------------------------------- #
    # Avoiding CORS                      #
    # ---------------------------------- #
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'PUT',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'}
        return ('', 204, headers)

    # ---------------------------- #
    # Set response header          #
    # ---------------------------- #
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'OPTIONS, PUT'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'

    try: 
        # ---------------------------------- #
        # 1. redis video_dict: video_dictionary
        # 1.1 video_dict = {'video_name1': 'url', ...}
        # ---------------------------------- #
        json_data = request.get_json()
        bbox_thd = json_data.get('bbox_threshold', None)
        class_thd = json_data.get('class_threshold', None)

        ai_setup = {}
        ai_setup['bbox_threshold'] = bbox_thd
        ai_setup['class_threshold'] = class_thd
        ai_setup['fps'] = 7.0
        r.hmset("ai_setup", ai_setup)
        
        return (json.dumps('ok'), 200, headers)
    
    except Exception as e:
        logging.warning("====>>: EDIT AI ERROR: " + str(e))
        return (json.dumps('ok'), 400, headers)


@app.route('/get_ai_data', methods=['GET'])
def get_ai_data(): 
    # ---------------------------------- #
    # Avoiding CORS                      #
    # ---------------------------------- #
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'}
        return ('', 204, headers)

    # ---------------------------- #
    # Set response                 #
    # ---------------------------- #
    response = {}
    try: 
        ai_setup = r.hgetall("ai_setup")
        response['bbox_threshold'] = ai_setup['bbox_threshold'.encode("utf-8")].decode("utf-8")
        response['class_threshold'] = ai_setup['class_threshold'.encode("utf-8")].decode("utf-8")
        response['fps'] = ai_setup['fps'.encode("utf-8")].decode("utf-8")

    except Exception as e: 
        logging.warning("====>>: GET AI ERROR: " + str(e))
        response['bbox_threshold'] = 0.0
        response['class_threshold'] = 0.0
        response['fps'] = 0.0

    # ---------------------------- #
    # Set response header          #
    # ---------------------------- #
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'
    return (json.dumps(response), 200, headers)

    
@app.route('/add_video_url', methods=['POST'])
def add_video_url():
    """Method for adding camera url
    
    Returns:
        [type] -- [description]
    """
    # ---------------------------------- #
    # Avoiding CORS                      #
    # ---------------------------------- #
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'}
        return ('', 204, headers)

    # ---------------------------------- #
    # 1. redis video_dict: video_dictionary
    # 1.1 video_dict = {'video_name1': 'url', ...}
    # ---------------------------------- #
    video_dict = r.hgetall("video_dict")
    json_data = request.get_json()
    video_name = json_data.get('video_name', None)
    video_url = json_data.get('video_url', None)
    point_y1 = json_data.get('y1', None)
    point_y2 = json_data.get('y2', None)

    # ---------------------------------- #
    # try to add the new camera url #
    # ---------------------------------- #
    video_id = str(uuid.uuid1())
    add_time = str(datetime.datetime.now())
    json_data = {}
    json_data['video_name'] = video_name
    json_data['video_url'] = video_url
    json_data['video_created'] = add_time
    video_dict[video_id] = json.dumps(json_data)
    r.hmset("video_dict", video_dict)

    # ---------------------------- #
    # add line point               #
    # ---------------------------- #
    point_dict = {}
    json_data = {}
    json_data['y1'] = point_y1
    json_data['y2'] = point_y2
    point_dict[video_id] = json.dumps(json_data)
    r.hmset("point_dict", point_dict)

    # ---------------------------- #
    # Set response header          #
    # ---------------------------- #
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, POST'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'
    return (json.dumps('ok'), 200, headers)


@app.route('/delete_video_url', methods=['DELETE'])
def delete_video_url():
    """Method for adding camera url
    
    Returns:
        [type] -- [description]
    """
    logging.warning("====>>: DELETE REQUEST")
    # ---------------------------------- #
    # Avoiding CORS                      #
    # ---------------------------------- #
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'DELETE',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'}
        return ('', 204, headers)
    
    # ---------------------------- #
    # Set response header          #
    # ---------------------------- #
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'OPTIONS, DELETE'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'

    try: 
        # ---------------------------------- #
        # 1. redis video_dict: video_dictionary
        # 1.1 video_dict = {'video_name1': 'url', ...}
        # ---------------------------------- #
        video_dict = r.hgetall("video_dict")
        video_id = request.args.get("id") #json_data.get('id', None)

        # ---------------------------------- #
        # try to delete the camera url       #
        # ---------------------------------- #
        r.hdel('point_dict', video_id)
        r.hdel('video_dict', video_id)
        return (json.dumps('ok'), 200, headers)

    except Exception as e: 
        logging.warning("====>>: DELETE ERROR: " + str(e))
        return (json.dumps('ok'), 400, headers)


@app.route('/edit_video_url', methods=['PUT'])
def edit_video_url():
    """Method for adding camera url
    
    Returns:
        [type] -- [description]
    """
    logging.warning("====>>: EDIT REQUEST")
    # ---------------------------------- #
    # Avoiding CORS                      #
    # ---------------------------------- #
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'PUT',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'}
        return ('', 204, headers)

    # ---------------------------- #
    # Set response header          #
    # ---------------------------- #
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'OPTIONS, PUT'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'

    try: 
        # ---------------------------------- #
        # 1. redis video_dict: video_dictionary
        # 1.1 video_dict = {'video_name1': 'url', ...}
        # ---------------------------------- #
        video_dict = r.hgetall("video_dict")
        json_data = request.get_json()
        video_name = json_data.get('video_name', None)
        video_url = json_data.get('video_url', None)
        video_id = json_data.get('id', None)
        point_y1 = json_data.get('y1', None)
        point_y2 = json_data.get('y2', None)

        # ---------------------------------- #
        # try to register the new camera url #
        # ---------------------------------- #
        json_data = json.loads(video_dict[video_id.encode("utf-8")].decode("utf-8"))
        add_time = json_data['video_created']
        r.hdel('video_dict', video_id)
        update_time = str(datetime.datetime.now())
        json_data = {}
        json_data['video_name'] = video_name
        json_data['video_url'] = video_url
        json_data['video_created'] = add_time
        json_data['video_updated'] = update_time
        video_dict[video_id.encode('utf-8')] = json.dumps(json_data)
        r.hmset("video_dict", video_dict)

        # ---------------------------- #
        # add line point               #
        # ---------------------------- #
        point_dict = {}
        json_data = {}
        json_data['y1'] = point_y1
        json_data['y2'] = point_y2
        point_dict[video_id] = json.dumps(json_data)
        r.hdel('point_dict', video_id)
        r.hmset("point_dict", point_dict)
        
        return (json.dumps('ok'), 200, headers)
    
    except Exception as e:
        logging.warning("====>>: EDIT ERROR: " + str(e))
        return (json.dumps('ok'), 400, headers)


@app.route('/get_video_list', methods=['GET'])
def get_video_list(): 
    # ---------------------------------- #
    # Avoiding CORS                      #
    # ---------------------------------- #
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'}
        return ('', 204, headers)

    # ---------------------------- #
    # Set response header          #
    # ---------------------------- #
    video_dict = r.hgetall("video_dict")
    point_dict = r.hgetall("point_dict")
    tmp_list = []

    for i in video_dict:
        tmp = {}
        tmp['id'] = i.decode("utf-8")
        json_data = json.loads(video_dict[i].decode("utf-8"))
        json_data_point = json.loads(point_dict[i].decode("utf-8"))
        tmp['video_name'] = json_data['video_name']
        tmp['video_url'] = json_data['video_url']
        tmp['date'] = json_data['video_created']
        tmp['status'] = 1
        tmp['y1'] = json_data_point['y1']
        tmp['y2'] = json_data_point['y2']
        tmp_list.append(tmp)
    
    # ---------------------------- #
    # Set response header          #
    # ---------------------------- #
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'
    return (json.dumps(tmp_list), 200, headers)


def messageReceived(methods=['GET', 'POST']):
    a = 0


def send_frame(): 
    while(True):
        for message in consumer:
            message = message.value

            frames = []
            for i in(message):
                frame = message[i]["b64"]
                status = message[i]["success"]
                video_name = message[i]["video_name"]

                if status:
                    frame = 'data:image/jpeg;base64,' + frame
                else: 
                    frame = ''
                    
                frames.append({"id": i, "name": video_name, "key": frame})
            
            if len(frames) > 0:
                frames = json.dumps(frames)
                socketio.emit('video_frame', frames, \
                            broadcast=True, callback=messageReceived)

            time.sleep(0.001)


@socketio.on('url')
def streamer(video_url, methods=['GET', 'POST']):
    logging.warning("====>>: INFO: new client")
    
    try:
        is_streaming_on = int(r.get('video_on'))
    except: 
        is_streaming_on = 1

    if is_streaming_on == 1:
        logging.warning("====>>: INFO: the sreaming is alredy live")
        pass 
    else:
        r.set('video_on', 1)
        logging.warning("====>>: INFO: Socket broadcaster started")
        send_frame()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8005, debug=True)
