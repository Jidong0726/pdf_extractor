## Usage

This software recognize pdf text files and images to extract information from both E-forms and Scanned copy, which relys on python library pdfminer and OCR engine Tesseract-OCR. For pdfminer and other related packages please just do "pip install" in python3.6. But for Tesseract-OCR, the curent version on pip seems not to support "whitelist" funcionality that used in this software, please go to https://github.com/tesseract-ocr/tesseract/releases/tag/4.1.1 to make sure you have the latest Tesseract 4.1.1 setup. The Tesseract will also need language data "eng.traineddata" to recognize english letters which I already attached in this git if it's missed in the source code. Please notice that this main code contained in "detect.py" can only recognize the number of Term 31 in a clear 1040 form. You may need to modify some rule based code in order to extract other information or apply it on other forms.


## Steps

1. Initialize your pdf_reader class by specifying popper path and tesseract path.
2. Read the file and get the extension. If ".pdf" then use pdfminer to detect whether it's an E-form or scanned picture. If other extension then directly use OCR engine. 
3. Apply different tools for different types of files. (pdfminer for standard E-form, OCR for scanned copy and other images). Config for OCR is
   ```python
   text=str(pytesseract.image_to_string(image, lang='eng', config='--psm 11 --oem 3 -c tessedit_char_whitelist=0123456789.-'))
   ```
   "psm 11" means "Sparse text. Find as much text as possible in no particular order", details refer to https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options. "tessedit_char_whitelist=0123456789.-" means only to extract letters from "=0123456789.-"
4. Rule based code. Split the extracted string and get the number.
