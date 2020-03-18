#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Created Date: Wednesday, March 11th 2020, 12:20:20 pm
# Author: Charlene Leong charleneleong84@gmail.com
# Last Modified: Monday, March 16th 2020, 8:52:04 am
###


import os
import requests
import json

from flask import Flask, render_template, request
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] =  os.path.join(basedir, 'static', 'uploads')

app.config.update(
    UPLOADED_PATH=app.config['UPLOAD_FOLDER'],
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
    DROPZONE_REDIRECT_VIEW='completed'  # set redirect view
)

dropzone = Dropzone(app)


@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        img_file = os.path.join(app.config['UPLOADED_PATH'], 'upload.png')
        f.save(img_file)

    return render_template('index.html')





@app.route('/completed')
def completed():
    
    addr = 'http://172.19.0.3:9090' # IP of backend
    URL = addr + '/mrcnn_predict'

    response = requests.get(URL)
    print(response.text)
    
    
    prediction_fname = os.path.join('static', 'prediction.png')
    return render_template('upload.html', prediction_img=prediction_fname)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
