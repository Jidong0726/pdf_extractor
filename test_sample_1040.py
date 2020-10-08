# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 23:07:41 2020

@author: jidong
"""

from detect import pdf_reader
import os

base_path = '1040_Samples/'
reader = pdf_reader(popper_path = r'D:\Release-20.09.0\poppler-20.09.0\bin', 
                        tesseract_path = r'D:\image_reader\tesseract.exe')
real_number = {'1': 94610.0, '2': 123316.0, '3': 5979.0, '4': 11147.0, '5': 43139.0, '6': 25576.0, 
               '7': 116054.0, '8': 105874.10, '9': 9635.0, '10': 42247.0, '11': 49020.0, '12': 31355.0}

results = []

for filename in os.listdir('1040_Samples'):
    if '.' in filename:
        if filename.endswith('.pdf') or filename.endswith('.PDF'):
            number = reader.text_reader(base_path+filename)
            if isinstance(number, str):
                number = reader.form_1040(base_path+filename)
        else:
            number = reader.form_1040(base_path+filename)
        print (filename, number)
