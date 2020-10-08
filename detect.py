# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 21:21:59 2020

@author: jidong
"""

from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import io

class pdf_reader(object):
    def __init__(self, popper_path, tesseract_path):
        self.popper_path = popper_path
        #pytesseract.pytesseract.tesseract_cmd = tesseract_path
        return
    
    def read_file(self, filepath):
        try:
            if filepath.endswith('.pdf') or filepath.endswith('.PDF'):
                images = self.pdf_pic_convert(filepath)
            else:
                images = [Image.open(filepath)]
        except:
            images = []
        return images
    
    def pdf_pic_convert(self, pdfname):
        #images = convert_from_path(pdfname, poppler_path= self.popper_path, use_pdftocairo=True)
        images = convert_from_path(pdfname, use_pdftocairo=True)
        return images
    
    def form_1040(self, filename):
        images = self.read_file(filename)
        if images == []:
            return ('cannot open target files')
        number = None
        for i in range(len(images)):
            image = images[i]
            text=str(pytesseract.image_to_string(image, lang='eng', config='--psm 11 --oem 3 -c tessedit_char_whitelist=0123456789.-'))
            if '\n\n31\n\n' in text:
                try:
                    number_str = text.split('\n\n31\n\n')[-1].split('\n')[0]
                    if number_str.endswith('.'):
                        number_str = number_str[:-1]
                    if number_str.count('.')>1:
                        number_str = number_str.replace('.', '', number_str.count('.')-1)
                    if len(number_str.split('.')[-1])>2:
                        number_str = number_str.replace('.', '')
                    number = float(number_str)
                except:
                    number = None
                if number is not None:
                    return number
                else:
                    return ('cannot recognize, please try to upload an E-document or a clear scanned copy')
        return 'cannot recognize, please try to upload an E-document or a clear scanned copy'

    def text_reader(self, filename):
        with open(filename, 'rb') as fh:
            for page in PDFPage.get_pages(fh, 
                                          caching=True,
                                          check_extractable=True):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                #fake_file_handle = io.BytesIO()
                converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8')
                page_interpreter = PDFPageInterpreter(resource_manager, converter)
                page_interpreter.process_page(page)
                
                text = fake_file_handle.getvalue()
                if 'Profit or Loss From Business' in text:
                    number = text.replace('\x0c','').split('.')[:-2]
                    try:
                        if len(number[-1])<=2:
                            res = number[-2]+'.'+number[-1]
                            res = float(res.replace(',',''))
                        else:
                            res = float(number[-1].replace(',',''))
                    except:
                        return ('cannot recognize, please try to upload an E-document or a clear scanned copy')
                    # close open handles
                    converter.close()
                    fake_file_handle.close()
                    return res
            converter.close()
            fake_file_handle.close()
        return ('cannot recognize, please try to upload an E-document or a clear scanned copy')

if __name__ == '__main__':
    file = '1040_Samples/1040 Schedule C 1.pdf'
    reader = pdf_reader(popper_path = r'D:\Release-20.09.0\poppler-20.09.0\bin', 
                        tesseract_path = r'D:\image_reader\tesseract.exe')
    
    #solu = reader.text_reader(file)
    solu = reader.form_1040(file)

    
    