import cv2 
import uuid
import json 
import base64
import datetime
import logging 
import numpy as np 
from kafka import KafkaConsumer
from flask import Flask, request
from flask_cors import CORS


# ---------------------------------- #
# setting kafka consumer             #
# ---------------------------------- #
"""
consumer = KafkaConsumer('cloud_handler_topic',
                        bootstrap_servers=['0.0.0.0:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='my-group',
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
"""
# ---------------------------------- #
# logging setup                      #
# ---------------------------------- #
logging.basicConfig(filename='/home/cloud_handler.log', 
                    filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')
logging.warning('======= SYSTEM WARMINGUP =========')

# ---------------------------------- #
# flask setup                        #
# ---------------------------------- #
app = Flask(__name__)
CORS(app)


@app.route('/total_page', methods=['GET'])
def total_page():
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
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'}
        return ('', 204, headers)

    # ---------------------------- #
    # Set response header          #
    # ---------------------------- #
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'
    
    resp = {}
    try: 
        num_item = request.args.get("item") 
        resp['total_page'] = 1
        return (json.dumps(resp), 200, headers)

    except Exception as e: 
        logging.warning("====>>: TOTAL_PAGE ERROR: " + str(e))
        return (json.dumps(resp), 400, headers)


@app.route('/get_item', methods=['GET'])
def get_item(): 
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
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'

    resp = {}
    try: 
        page = request.args.get("page") 
        num_item = int(request.args.get("limit"))
        
        data = []
        for i in range(num_item): 
            tmp = {}
            tmp['id'] = str(uuid.uuid1())
            tmp['camera'] = 'kilang depan'
            tmp['helm'] = 0
            tmp['jacket'] = 0
            tmp['date'] = str(datetime.datetime.now())
            data.append(tmp)

        resp['data'] = data
        return (json.dumps(resp), 200, headers)

    except Exception as e: 
        logging.warning("====>>: TOTAL_PAGE ERROR: " + str(e))
        return (json.dumps(resp), 400, headers)


@app.route('/get_image', methods=['GET'])
def get_image(): 
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
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'

    resp = {}
    try: 
        obj_id = request.args.get("id") 
        
        full_img = np.zeros((400, 400, 3)).astype(np.uint8)
        full_img = cv2.imencode('.jpg', full_img)[1]
        full_img = base64.b64encode(full_img).decode()
        person_img = np.zeros((200, 80, 3)).astype(np.uint8)
        person_img = cv2.imencode('.jpg', person_img)[1]
        person_img = base64.b64encode(person_img).decode()

        resp['full_image'] = 'data:image/jpeg;base64,' + full_img
        resp['person'] = 'data:image/jpeg;base64,' + person_img
        return (json.dumps(resp), 200, headers)

    except Exception as e: 
        logging.warning("====>>: TOTAL_PAGE ERROR: " + str(e))
        return (json.dumps(resp), 400, headers)


if __name__ == '__main__':
    app.run(app, host='0.0.0.0', port=8004, debug=True)

