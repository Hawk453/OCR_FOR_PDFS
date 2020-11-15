# -*- coding: utf-8 -*-
"""Author: Saksham Madan
   Date: 15/11/2020

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X6kNyAWVqiX8qWVimWfx2pUjgiRCeuW3
"""

# Commented out IPython magic to ensure Python compatibility.
!apt-get install poppler-utils 
!pip install pdf2image
!pip install opencv-python
!sudo apt install tesseract-ocr
!pip install pytesseract
!pip install pillow

#modules to be imported

import cv2
import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
import os

def image_processing(img):
    # get grayscale image
    img1 =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # noise removal
    img2 = cv2.medianBlur(img1,5)
 
    #thresholding
    #return cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return cv2.adaptiveThreshold(img2, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

def ocr_to_text(img):
    custom_config = r'--oem 1 --psm 6'
    return pytesseract.image_to_string(img, config=custom_config)

def text_generation(x_data):

  text = []

  for x in x_data:
      
      a = image_processing(x)
      b = ocr_to_text(a)
      
      text.append(b)

  return text

def pdf_to_images(pdfs):
      
      #pages = convert_from_path(pdfs, 500)
      #depending on the format fo the pdf use either of them, if .pdf and format word use above
      #If format is in bytes use below
      #change the dpi(here it is 500) depending on the resolution of the scanned document
      pages = convert_from_bytes(pdfs.read(), 500)

      x_data = []

      i = 1
      for page in pages:
          image_name = "Page_" + str(i) + ".jpg"  
          page.save(image_name, "JPEG")
          image = cv2.imread(image_name)
          x_data.append(image)
          i = i+1
      
      text = []

      text = text_generation(x_data)
      
      
      i=1
      for page in pages:
          os.remove("Page_" + str(i) + ".jpg")
          i = i+1

          
      return text

def _main_(download_pdf):

    text = []
    pdfs = download_pdf
    text = pdf_to_images(pdfs)
    
    return text

#the output will be saved in the text file

text = []
text = _main_("<your_pdf_path_and_name>")
for t in text:
    
    f = open("text.txt", "a+")
    f.write(t)
    

f.close()
