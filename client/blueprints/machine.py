import requests
import base64
import argparse
import json
from flask import Flask,render_template,request,Blueprint

machine = Blueprint('machine', __name__)

parser = argparse.ArgumentParser(description="Predict a label for an image.")
parser.add_argument("image", help="Path to your image file.")
args = parser.parse_args()

@machine.route('/machine', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return render_template("upload.html")
        file1 = request.files['file1']

        base64_encoded_data = base64.b64encode(file1.read())
        base64_message = base64_encoded_data.decode('utf-8')
        url = 'http://127.0.0.1:5000/girlgroup/game'
        body = {'base64': base64_message}
        prediction = requests.post(url, json = body).json()
         
        return render_template("prediction.html",predic = prediction)


    
    return render_template("upload.html")

