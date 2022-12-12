

# find color lower/higher range
# find code to run over all 

import cv2
import numpy as np
from mss import mss
from PIL import Image, ImageGrab
import time
    
WINDOW_BOX = (0, 0, 1920, 1080)


def convert_HSV(h, s, v):
    """
    Convert HSV values in opencv format
    - normal HSV: 0-360, 0-100, 0-100 format
    - opencv HSV: 0-179, 0-255, 0-255 format
    """
    converted_hsv = [h/2, s*255/100, v*255/100]

    return converted_hsv

def run_rubie_detect(light_red_range, dark_red_range):
    with mss() as sct:
        while True:
            # ImageGrab return RGB
            image = ImageGrab.grab(bbox=WINDOW_BOX)
            # Convert RGB -> BGR (opencv default)
            GBR_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            # Convert image to HSV
            hsv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)
            # hsv_image = GBR_image.convert('HSV')
            hsv_screen = (np.array(hsv_image))
            # build mask 
            light_red_mask = generate_mask(hsv_screen, light_red_range)
            dark_red_mask = generate_mask(hsv_screen, dark_red_range)
            # combine the masks
            masks = light_red_mask + dark_red_mask
            # filter image with mask
            result = cv2.bitwise_and(hsv_screen, hsv_screen, mask=masks)
            # resize the screen
            result = cv2.resize(result, (960, 540))
            cv2.imshow("mask_screen", result)
            # stop
            if cv2.waitKey(33) & 0xFF in (
                    ord('q'), 
                    27, 
                ):
                    break
    cv2.destroyAllWindows()

def generate_mask(screen, range):
    """
    Create opencv mask using range
    """
    return cv2.inRange(screen, range[0], range[1])

def print_mask_range(range):
    lower = range[0]
    upper = range[1]
    
    print(f"mask: {lower[0]}~{upper[0]} | {lower[1]}~{upper[1]} | {lower[2]}~{upper[2]}")

if __name__ == "__main__":
    # LIGHT_RED_HSV = [[0, 80, 10], [3, 100, 40]]
    # DARK_RED_HSV = [[350, 50, 20], [359, 100, 70]]

    LIGHT_RED_HSV = [[0, 80, 10], [3, 100, 40]]
    DARK_RED_HSV = [[0, 0, 0], [0, 0, 0]]

    # set mask ranges
    light_red_range = list(map(lambda a: np.array(convert_HSV(*a)), LIGHT_RED_HSV))
    dark_red_range = list(map(lambda a: np.array(convert_HSV(*a)), DARK_RED_HSV))

    print_mask_range(light_red_range)
    print_mask_range(dark_red_range)

    run_rubie_detect(light_red_range, dark_red_range)
    