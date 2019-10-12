import cv2
import time
import json
import redis
import pickle
import base64
import datetime
import logging
from kafka import KafkaConsumer
from flask import Flask, request, render_template
from flask_socketio import SocketIO


# ---------------------------------- #
# setting kafka consumer             #
# ---------------------------------- #
consumer = KafkaConsumer('ai_topic',
                        bootstrap_servers=['localhost:9092'],
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
socketio = SocketIO(app, cors_allowed_origins="*")
# ---------------------------------- #
# logging setup                      #
# ---------------------------------- #
logging.basicConfig(filename='/home/broadcaster.log', filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('======= SYSTEM WARMINGUP =========')



@app.route('/web')
def web():
    """ Endpoint for rendering the homepage html
    
    Returns:
        [hmtl] -- html webpage
    """
    tm = datetime.datetime.now()
    tm = tm.strftime("%c")
    print ('---------')
    logging.warning("===>>> A. The main endpoint was requested" + tm)
    return render_template('index.html')


@app.route('/', methods=['POST'])
def sessions():
    """ Endpoint for init first request
    
    Returns:
        [hmtl] -- html webpage
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

    # ---------------------------- #
    # Set response header          #
    # ---------------------------- #
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, POST'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'
    print ('=============================>>><<<<')
    return (json.dumps('ok'), 200, headers)
    

@app.before_first_request
def before_first_request_func():
    """Method for setting the video status 'video_on' on redis to zero,
       Called when the first user open a homepage for the first time
    """
    is_streaming_on = int(r.get('video_on'))
    print (is_streaming_on)
    r.set('video_on', 0)
    is_streaming_on = int(r.get('video_on'))
    print (is_streaming_on)
    tm = datetime.datetime.now()
    tm = tm.strftime("%c")
    logging.warning("===>>> B. The data of 'video_on' in redis \
                     was reinitialized: " + tm)


@app.route('/add_video_url', methods=['POST'])
def add_video_url():
    print('>>>>>>>>>>>')
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

    # ---------------------------------- #
    # try to register the new camera url #
    # ---------------------------------- #
    if len(list(video_dict.keys())) == 0:
        video_dict = {}
        video_dict[video_name] = video_url
        r.hmset("video_dict", video_dict)
    else:
        video_dict[video_name] = video_url
        r.hmset("video_dict", video_dict)

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


def messageReceived(methods=['GET', 'POST']):
    a = 0


def send_frame(): 
    while(True):
        for message in consumer:
            message = message.value
            
            frames = []
            for i in(message):
                frame = message[i]
                frame = 'data:image/jpeg;base64,' + frame
                frames.append({"id": i, "key": frame})
            
            if len(frames) > 0:
                frames = json.dumps(frames)
                #print (frames)
                socketio.emit('video_frame', frames, \
                            broadcast=True, callback=messageReceived)
                time.sleep(0.04)


@socketio.on('url')
def streamer(video_url, methods=['GET', 'POST']):
    print ('------------------')
    print ('new client')
    print ('------------------')

    is_streaming_on = int(r.get('video_on'))
    if is_streaming_on == 1:
        print ('the sreaming is alredy live')
        pass 
    else:
        r.set('video_on', 1)
        print ('=====>>> called')
        send_frame()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8005, debug=True)
