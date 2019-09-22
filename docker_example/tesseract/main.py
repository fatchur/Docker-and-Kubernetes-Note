import io
import cv2
import json 
import base64
import numpy as np
import pytesseract
from PIL import Image
from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def stringToImage(base64_string):
    """[summary]
    
    Arguments:
        base64_string {str} -- base64 image string
    
    Returns:
        [type] -- [description]
    """
    try:
        imgData = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(imgData)), True
    except:
        return None, False


def preprocess_black_white(img):
    """[summary]
    
    Arguments:
        img {[type]} -- [description]
    """
    gray = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite('tmp.jpg', gray)


@app.route("/get_text", methods=['GET', 'POST'])
def get_text():
    # ---------------------------- #
    # Avoiding CORS                #
    # ---------------------------- #
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
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

    resp = {}
    
    # ---------------------------- #
    # Process the request data     #
    # ---------------------------- #
    json_data = request.get_json()
    base64string = json_data.get('image', None)
    img, status = stringToImage(base64string) 

    if status:
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('tmp.jpg', img)

        text = pytesseract.image_to_string(Image.open('tmp.jpg'))
        resp['text'] = text
        return (json.dumps(resp), 200, headers)
    else:
        resp['text'] = "image fail to handle"
        return (json.dumps(resp), 400, headers)



if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8080
    app.run(threaded=True, port=8080)