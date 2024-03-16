import pytesseract
from pytesseract import Output
from PIL import Image
import cv2
import numpy as np

def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


img_path1 = "captcha2.png"

img = cv2.imread(img_path1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Dilate
kernel = np.ones((3, 3), np.uint8)
dilated = cv2.dilate(thresh, kernel, iterations=1)

invert = 255 - dilated
text = pytesseract.image_to_string(invert, lang="eng", config="--psm 6")
text = cleanup_text(text)

print(text)

cv2.imwrite("cleaned.png", invert)
