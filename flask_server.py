# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 18:26:37 2020

@author: jidong
"""
from flask import abort, Flask, request
import warnings
from detect import pdf_reader
import os

ALLOWED_IPS = ['127.0.0.1','']
BASE_URL = '/home/grmds/websites/alcppp.com/sites/default/files/private/webform/apply_for_ppp_loan'

app = Flask(__name__)

@app.errorhandler(403)
def permission_error(e):
    return '403 error'

@app.before_request
def limit_remote_addr():
    client_ip = str(request.remote_addr)
    valid = False
    for ip in ALLOWED_IPS:
        if client_ip.startswith(ip) or client_ip == ip:
            valid = True
            break
    if not valid:
        abort(403)

@app.route('/detect_1040_schedule_C/<string:filename>', methods=['GET', 'POST'])
def operate_detector(filename):
    warnings.filterwarnings("ignore")
    reader = pdf_reader(popper_path = r'D:\Release-20.09.0\poppler-20.09.0\bin', 
                        tesseract_path = r'D:\image_reader\tesseract.exe')
    path = os.path.join(BASE_URL, filename)
    if filename.endswith('.pdf') or filename.endswith('.PDF'):
            number = reader.text_reader(path)
            if isinstance(number, str):
                number = reader.form_1040(path)
    else:
        number = reader.form_1040(path)
    return number


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)