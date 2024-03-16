from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import urllib.request
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from PIL import Image
import cv2


ORI_URL = "http://app.vr.org.vn/ptpublic/"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://app.vr.org.vn",
    "Referer": "http://app.vr.org.vn/ptpublic/thongtinptpublic.aspx",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/122.0.0.0",
}


def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def ocr(img):
    text = pytesseract.image_to_string(img, lang="eng")
    return text


def send_request(url):
    try:
        # Create a new instance of the Firefox driver
        driver = webdriver.Firefox()
        # Go to the specified URL
        driver.get(url)

        txtBienDK = driver.find_element("name", "txtBienDK")
        txtBienDK.send_keys("51A84920T")

        TxtSoTem = driver.find_element("name", "TxtSoTem")
        TxtSoTem.send_keys("DB-0365271")

        # Read image from image url
        img_url = get_image_capcha(url)
        img = load_image(img_url)
        # Save the image
        cv2.imwrite("captcha.png", img)
        text = ocr(img)
        # Processing text
        text = cleanup_text(text)
        print(text)

        txtCaptcha = driver.find_element("name", "txtCaptcha")
        txtCaptcha.send_keys(text)

        # Submit the form by clicking the button
        CmdTraCuu = driver.find_element("name", "CmdTraCuu")
        CmdTraCuu.click()

        # Get the page source
        page_source = driver.page_source

        # Close the browser
        # driver.quit()
        return page_source
    except Exception as e:
        print(e)
        return None


def load_image(image_url):
    # Load the image from the URL
    image = requests.get(image_url, headers=headers, allow_redirects=True).content
    # Decode the image
    nparr = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def get_image_capcha(url):
    response = requests.get(url, headers=headers, allow_redirects=True).content
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response, "html.parser")
    # Find the CAPTCHA image tag
    captcha_img_tag = soup.find("img", id="captchaImage")
    # Extract the 'src' attribute which contains the URL of the CAPTCHA image
    captcha_img_url = captcha_img_tag["src"]
    img_url = ORI_URL + captcha_img_url
    return img_url


if __name__ == "__main__":
    url = "http://app.vr.org.vn/ptpublic/thongtinptpublic.aspx"
    print(send_request(url))
