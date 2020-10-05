# Script that performs random walks in google streetview
# For the rotation to work, the broser window must be in focus - for now
from time import sleep
from random import randint

from pyautogui import keyDown, keyUp, PAUSE, KEYBOARD_KEYS
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com/maps/@39.7273647,-104.9624829,3a,75y,290.76h,90t/data=!3m6!1e1!3m4!1sehmBeTbY66ojPB1Jz2bfxA!2e0!7i16384!8i8192")
keys = webdriver.common.keys.Keys
sleep(2)
# focus on the map image
driver.find_element_by_class_name('widget-scene-canvas').click()
sleep(2)

past_url = ""
arrow_key = "left"
past_locations = []
while True:
    curr_url = driver.current_url
    lat_start = curr_url.find("@")
    lat_end = curr_url.find(",")
    lng_end = curr_url.find(",", lat_end+1)
    # Parse lat/lng from url
    if lat_start != -1 and lat_end != -1 and lng_end != -1:
        lat_lng = curr_url[lat_start+1:lng_end]
        past_locations.append(lat_lng)
    # Write locations to file every 100 moves
    if len(past_locations) > 100:
        with open("locations.txt", "a") as fp:
            fp.write(' '.join(past_locations))
        past_locations.clear()
    # If we didn't move at the last turn, rotate to get unstuck
    if curr_url == past_url:
        keyDown(arrow_key)
        sleep(randint(1,4))
        keyUp(arrow_key)
        if arrow_key == "left":
            arrow_key = "right"
        else:
            arrow_key = "left"
    # Move forward in the street view and wait 2 seconds
    driver.find_element_by_class_name('widget-scene-canvas').send_keys(keys.UP)
    past_url = curr_url
    sleep(2)