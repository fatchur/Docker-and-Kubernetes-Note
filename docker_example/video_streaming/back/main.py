import datetime
import logging
import cv2 
import time
import base64
from flask import Flask, render_template
from flask_socketio import SocketIO
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def sessions():
    print ('========')
    return render_template('index.html')


def messageReceived(methods=['GET', 'POST']):
    print('frame transmitted')


@app.before_first_request
def before_first_request_func():
    r.set('video_on', 0)
    print ('executed')


def send_frame(): 
    while(True):
        cap = cv2.VideoCapture('output.avi')
        
        if cap.isOpened():
            while(True):
                ret, frame = cap.read()

                if ret == True:
                    frame = cv2.imencode('.jpg', frame)[1]
                    frame = base64.b64encode(frame).decode()
                    frame = 'data:image/jpeg;base64,' + frame
                    socketio.emit('video_frame', frame, broadcast=True, callback=messageReceived)
                    time.sleep(0.05)
                
                else:
                    tm = datetime.datetime.now()
                    tm = tm.strftime("%c")
                    print ("INFO enter false1--")
                    logging.warning('--->> Restart video capture  else : ' + tm)
                    cap.release()
                    break

        else:
            tm = datetime.datetime.now()
            tm = tm.strftime("%c")
            print ("INFO enter false2--")
            logging.warning('--->> Restart video capture try catch  : ' + tm )
            cap.release()


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
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
