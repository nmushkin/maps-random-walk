import os
from math import floor

from keras.models import load_model
from PIL import Image
import numpy as np

from classifier import IMAGE_SIZE
from walker import MapWalker

CAM_LOCATION_FILE = "data/cam_loc_00.txt"
SAVED_SHOTS_DIR = "data/saved_pics"
TILE_SIZE = 200

def step_factory(clf_model):
    model = load_model(clf_model)
    def step_function(latlng, screenshot):
        rgb_tiles, gray_tiles = image_to_tiles(screenshot)
        print(gray_tiles.shape)
        gray_tiles = gray_tiles.reshape(-1, IMAGE_SIZE, IMAGE_SIZE, 1)
        print(gray_tiles.shape)
        labels = model.predict(gray_tiles)
        for tile_no, label in enumerate(labels):
            if np.argmax(label) == 1:
                print(latlng)
                gray_tile = gray_tiles[tile_no]
                rgb_tile = rgb_tiles[tile_no]
                with open(CAM_LOCATION_FILE, "a") as fp:
                    fp.write(latlng + '\n')
                image = Image.fromarray(rgb_tile.astype(np.uint8)).convert("RGB")
                fname = f'{latlng}-{tile_no}'
                image.save(fp=(f'{os.path.join(SAVED_SHOTS_DIR, fname)}.jpeg'))
    return step_function

def image_to_tiles(image):
    img = Image.open(image)
    img_rgb = np.array(img.convert('RGB'))
    img_gray = np.array(img.convert('L'))
    # img = img / 255
    y_num = floor(img_gray.shape[1] / TILE_SIZE)
    x_num = floor(img_gray.shape[0] / TILE_SIZE)
    indices = [(x, y) for x in range(0, x_num) for y in range(0, y_num) if not_corner(x, y, x_num, y_num)]
    rgb_tiles = np.array([img_rgb[x*TILE_SIZE: (x+1)*TILE_SIZE, y*TILE_SIZE: (y+1)*TILE_SIZE] for x, y in indices])
    gray_tiles = np.array([img_gray[x*TILE_SIZE: (x+1)*TILE_SIZE, y*TILE_SIZE: (y+1)*TILE_SIZE] for x, y in indices])
    print(rgb_tiles.shape, gray_tiles.shape)
    return rgb_tiles, gray_tiles

def not_corner(x, y, x_num, y_num):
    if x < 3 and y < 3:
        return False
    if x < 3 and y > y_num - 3:
        return False
    if x > x_num - 3 and y < 3:
        return False
    if x > x_num - 3 and y > y_num - 3:
        return False
    return True

step_func = step_factory("cam_model_7.h5")
start_url = "https://www.google.com/maps/@47.6170462,-122.3388064,3a,75y,133.69h,84.43t/data=!3m6!1e1!3m4!1s3TdyPHnia_hm69GNsaA-1w!2e0!7i16384!8i8192"
map_walker = MapWalker(maps_url=start_url, location_f="first_walk.txt", step_function=step_func)
map_walker.run()

