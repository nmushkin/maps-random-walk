import base64
import requests
import os
import re
from time import sleep

# from bs4 import BeautifulSoup
from selenium import webdriver

def download_image(path, filename, url):
    if not os.path.isdir(path):
        os.makedirs(path)
    extension = url.split(".")[-1]
    full_path = os.path.join(path, filename)
    req = requests.get(url)
    if req.status_code == 200:
        with open(full_path, 'wb') as f:
            for chunk in req:
                f.write(chunk)

def save_base_64_src(path, filename, src):
    if not src:
        return
    if not os.path.isdir(path):
        os.makedirs(path)
    extension = src[src.index("/") + 1 : src.index(";")]
    src = src[src.index(","):].encode('utf-8')
    full_path = f'{os.path.join(path, filename)}.{extension}'
    print(full_path)
    with open(full_path, "wb") as fp:
        fp.write(base64.decodebytes(src))

def print_attrs(element):
    attrs=[]
    for attr in element.get_property('attributes'):
        attrs.append([attr['name'], attr['value']])
    print(attrs)


page_url = "https://www.google.com/search?q=brooklyn+street+trees&tbm=isch&ved=2ahUKEwjW5MyVvKDsAhX6KjQIHU4RCcYQ2-cCegQIABAA&oq=brooklyn+street+trees&gs_lcp=CgNpbWcQAzIECAAQGDoHCAAQsQMQQzoECAAQQzoKCAAQsQMQgwEQQzoFCAAQsQM6AggAOggIABCxAxCDAToGCAAQCBAeUJs4WM5MYJ5OaABwAHgBgAGaBIgB1xuSAQswLjUuNC4xLjIuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=caZ8X5boBfrV0PEPzqKksAw&bih=939&biw=1680&rlz=1C5CHFA_enUS752US752&hl=en&hl=en"
num_pages = 80
img_num = 2411
driver = webdriver.Chrome()
page = driver.get(page_url)
last_scroll = driver.execute_script("return document.body.scrollHeight")
for page in range(0, num_pages):
    sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)
    scroll = driver.execute_script("return document.body.scrollHeight")
    if last_scroll == scroll:
        break
    last_scroll = scroll

imgs = driver.find_elements_by_tag_name("img")
print(len(imgs))
for img in imgs:
    img_src = img.get_attribute("src")
    data_src = img.get_attribute("data-src")
    if img_src and img_src.find("data") != -1:
        print(img_num)
        save_base_64_src("./data/images/cameras", f'cam{img_num}', img_src)
        img_num += 1
    elif data_src and data_src.find("http") != -1:
        print(img_num)
        download_image("./data/images/cameras", f'cam{img_num}.jpeg', data_src)
        img_num += 1
