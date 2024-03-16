import pytesseract
from pytesseract import Output
from PIL import Image
import cv2
import easyocr
reader = easyocr.Reader(['ch_sim','en'], gpu=False)

def cleanup_text(text):
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()

img_path1 = 'captcha4.png'
img = cv2.imread(img_path1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)

result = reader.readtext(blur)
print(result)
