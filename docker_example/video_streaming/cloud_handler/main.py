import cv2 
import uuid
import json
import math 
import base64
import datetime
import logging 
import numpy as np 
from flask import Flask, request
from flask_cors import CORS
from comdutils.file_utils import get_filenames



def process_filename(filenames): 
    """[summary]
    
    Arguments:
        filenames {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    filenames.reverse()

    file_list = []
    for i in filenames: 
        id = i[20:55]
        tmp = {}
        tmp['id'] = id

        if ('_VIOLATION___' in i) or ('_VIOLATION_VIOLATION_' in i): 
            tmp['jacket_violation'] = 0 #violation
        else: 
            tmp['jacket_violation'] = 1

        if ('__VIOLATION_' in i) or ('_VIOLATION_VIOLATION_' in i): 
            tmp['helm_violation'] = 0 #violation
        else: 
            tmp['helm_violation'] = 1
        file_list.append(tmp)

    return file_list


def search_by_id(filenames, id): 
    """[summary]
    
    Arguments:
        filenames {[type]} -- [description]
        id {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    selected = ''
    for i in filenames: 
        if id in i: 
            selected = i 
            break
    return selected


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
        num_item = int(request.args.get("item"))
        filenames = get_filenames('/home/saver/res/full/')
        total_item = len(filenames)
        total_page = math.ceil(total_item/num_item)
        if total_page == 0: 
            total_page = 1

        resp['total_page'] = total_page
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
        page = int(request.args.get("page"))
        num_item = int(request.args.get("limit"))

        # ---------------------------------- #
        # get the list of saved image filenames 
        # preprocess the ID, jacket and helm violation
        # ---------------------------------- #
        filenames = get_filenames('/home/saver/res/full/')
        filenames = process_filename(filenames)

        # ---------------------------------- #
        # get the total page
        # ---------------------------------- #
        total_item = len(filenames)
        total_page = math.ceil(total_item/num_item)
        if total_page == 0: 
            total_page = 1
        
        # ---------------------------------- #
        # prepare the response
        # ---------------------------------- #
        data = []
        for i in range(num_item):
            try: 
                filenames_idx = page * num_item + i
                tmp = {}
                tmp['id'] = filenames[filenames_idx]['id']
                tmp['camera'] = 'kilang depan'
                tmp['helm'] = filenames[filenames_idx]['helm_violation']
                tmp['jacket'] = filenames[filenames_idx]['jacket_violation']
                tmp['date'] = str(datetime.datetime.now())
                data.append(tmp) 
            except Exception as e:
                logging.warning(str(e))
                
        resp['data'] = data
        resp['total_page'] = total_page
        return (json.dumps(resp), 200, headers)

    except Exception as e: 
        logging.warning("====>>: GET_ITEM ERROR: " + str(e))
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
        # ---------------------------- #
        # Get the argument             #
        # ---------------------------- #
        obj_id = request.args.get("id") 
        # ---------------------------- #
        # process the full image and cropped filename   
        # ---------------------------- #
        filenames = get_filenames('/home/saver/res/full/')
        filename_full = search_by_id(filenames, obj_id)
        filename_cropped = filename_full[:-8] + 'cropped.jpg'
        
        # ---------------------------- #
        # read both image              # 
        # ---------------------------- #
        full_img = cv2.imread('/home/saver/res/full/' + filename_full)
        full_img = cv2.imencode('.jpg', full_img)[1]
        full_img = base64.b64encode(full_img).decode()

        person_img = cv2.imread('/home/saver/res/cropped/' + filename_cropped)
        person_img = cv2.imencode('.jpg', person_img)[1]
        person_img = base64.b64encode(person_img).decode()

        resp['full_image'] = 'data:image/jpeg;base64,' + full_img
        resp['person'] = 'data:image/jpeg;base64,' + person_img
        return (json.dumps(resp), 200, headers)

    except Exception as e: 
        logging.warning("====>>: GET_IMAGE ERROR: " + str(e))
        return (json.dumps(resp), 400, headers)


if __name__ == '__main__':
    app.run(app, host='0.0.0.0', port=8004, debug=True)

