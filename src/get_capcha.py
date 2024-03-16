from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import urllib.request
import cv2
import numpy as np


ORI_URL = "http://app.vr.org.vn/ptpublic/"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://app.vr.org.vn",
    "Referer": "http://app.vr.org.vn/ptpublic/thongtinptpublic.aspx",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/122.0.0.0",
}


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
    captcha_img_url = get_image_capcha(url)
    img = load_image(captcha_img_url)
    cv2.imwrite("captcha3.png", img)
