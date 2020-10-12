# Class / script that performs random walks in google streetview
# For the rotation to work, the broser window must be in focus - for now
from io import BytesIO
from time import sleep
from random import randint
from threading import Thread
from datetime import datetime, timedelta

from pyautogui import keyDown, keyUp, PAUSE, KEYBOARD_KEYS
from selenium import webdriver


class MapWalker():

    def __init__(self, maps_url, location_f="locations.txt", step_function=None):
        self.maps_start = maps_url
        self.driver = webdriver.Chrome()
        self.keys = webdriver.common.keys.Keys
        self.location_file = location_f
        self.step_function = step_function
        self.turn_direction = "left"

    def run(self):
        t = Thread(target=self.walk)
        t.start()
        t.join()

    def walk(self, step_secs=2, timeout=timedelta(hours=1)):
        locations = []
        last_url = ""
        tries = 0
        action_chains = webdriver.ActionChains(self.driver)
        self.driver.get(self.maps_start)
        sleep(1)
        # focus on the map image and allow for page update
        map_element = self.driver.find_element_by_class_name('widget-scene-canvas')
        map_element.click()
        sleep(2)
        while datetime.now() < datetime.now() + timeout:
            curr_url = self.driver.current_url
            lat_long = self.get_latlng(curr_url)
            if lat_long:
                locations.append(lat_long)
                keyDown("left")
                sleep(1)
                keyUp("left")
                screen_1 = BytesIO(self.driver.get_screenshot_as_png())
                keyDown("right")
                sleep(1.9)
                keyUp("right")
                screen_2 = BytesIO(self.driver.get_screenshot_as_png())
                keyDown("left")
                sleep(1.04)
                keyUp("left")
                if self.step_function:
                    self.step_function(lat_long, screen_1)
                    self.step_function(lat_long, screen_2)
            if last_url == curr_url:
                tries += 1
            turn = tries > 2
            if turn:
                tries = 0
            self.take_step(turn)
            # Write locations to file every 100 moves
            if len(locations) > 100:
                self.save_locations(locations)
            last_url = curr_url
            sleep(step_secs)

    def take_step(self, turn=False):
        # If we didn't move on the last turn, rotate to get unstuck
        if turn:
            keyDown(self.turn_direction)
            sleep(randint(1,4))
            keyUp(self.turn_direction)
            if self.turn_direction == "left":
                self.turn_direction = "right"
            else:
                self.turn_direction = "left"
        # Move forward in the street view and wait 2 seconds
        self.driver.find_element_by_class_name('widget-scene-canvas').send_keys(self.keys.UP)
        sleep(.5)
        self.driver.find_element_by_class_name('widget-scene-canvas').send_keys(self.keys.UP)

    def save_locations(self, location_list):
        with open(self.location_file, "a") as fp:
            fp.write(' '.join(location_list))

    def get_latlng(self, url):
        lat_start = url.find("@")
        lat_end = url.find(",")
        lng_end = url.find(",", lat_end+1)
        # Parse lat/lng from url
        if lat_start != -1 and lat_end != -1 and lng_end != -1:
            lat_lng = url[lat_start+1:lng_end]
            return lat_lng
        return None
