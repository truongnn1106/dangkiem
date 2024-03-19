from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import cv2
import numpy as np
from PIL import Image
import PIL.Image as ImageV2
import numpy as np
from dotenv import load_dotenv
import os
import google.generativeai as genai
import io
import cv2
import time
import base64
from urllib.request import Request, urlopen


load_dotenv()

ORI_URL = "http://app.vr.org.vn/ptpublic/"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://app.vr.org.vn",
    "Referer": "http://app.vr.org.vn/ptpublic/thongtinptpublic.aspx",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/122.0.0.0",
}


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(im):
    if im is not None:

        pil_im = Image.fromarray(np.uint8(im))
        b = io.BytesIO()
        pil_im.save(b, format="PNG")
        image_value = b.getvalue()

        image_parts = [
            {
                "data": image_value,
                "mime_type": "image/png",
            }
        ]
        return image_parts
    else:
        raise ValueError("Image is empty")


def send_request(url):
    try:
        # Create a new instance of the Firefox driver
        driver = webdriver.Firefox()
        # Go to the specified URL
        driver.get(url)

        img_url = driver.find_element("id", "captchaImage").get_attribute("src")
        print(img_url)

        txtBienDK = driver.find_element("name", "txtBienDK")
        txtBienDK.send_keys("51A84920T")

        TxtSoTem = driver.find_element("name", "TxtSoTem")
        TxtSoTem.send_keys("DB-0365271")

        im = load_image(img_url)
        image = input_image_setup(im)

        prompt = 'You are an expert in understanding captcha. You will receive an input image as captcha. You will output is a text in image. Dont explain any more. I need to a text in ""'
        input = "A photo of a captcha"
        captcha = get_gemini_response(input, image, prompt)
        captcha = cleanup_text(captcha)
        captcha = captcha.replace('"', "")
        print(captcha)

        txtCaptcha = driver.find_element("name", "txtCaptcha")
        txtCaptcha.send_keys(captcha)
        time.sleep(1)

        # Submit the form by clicking the button
        CmdTraCuu = driver.find_element("name", "CmdTraCuu")
        CmdTraCuu.click()

        # Get the page source
        page_source = driver.page_source

        time.sleep(2)
        # Close the browser
        driver.quit()
        return page_source
    except Exception as e:
        print(e)
        return None


def decode_base64_image(base64_string):
    if "," in base64_string:
        base64_string = base64_string.split(",")[-1]
    imgdata = base64.b64decode(base64_string)
    image = np.frombuffer(imgdata, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def load_image(inp):
    try:
        if "http" in inp:
            img_url = inp.replace(" ", "%20")
            req = urlopen(Request(img_url, headers={"User-Agent": "XYZ/3.0"}))
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1)
        else:
            img = decode_base64_image(inp)
        return img
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    url = "http://app.vr.org.vn/ptpublic/thongtinptpublic.aspx"
    print(send_request(url))
