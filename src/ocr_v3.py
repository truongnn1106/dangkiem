import cv2
import pytesseract
import numpy as np
from pytesseract import Output

def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

img = cv2.imread('captcha2.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# Dilate
kernel = np.ones((2, 2), np.uint8)
dilated = cv2.dilate(thresh, kernel, iterations=1)
invert = 255 - dilated

d = pytesseract.image_to_data(invert, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
    if (d['text'][i] != ""):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        # Expand ROI
        x -= 5
        y -= 5
        w += 5
        h += 10
        text = pytesseract.image_to_string(invert[y:y+h, x:x+w], config='--psm 6')
        text = cleanup_text(text)
        print(text)
cv2.imwrite('output.png', invert[y:y+h, x:x+w])