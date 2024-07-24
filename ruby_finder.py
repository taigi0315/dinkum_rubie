

# find color lower/higher range
# find code to run over all 

import cv2
import numpy as np
from mss import mss
from PIL import Image, ImageGrab
import simpleaudio as sa
import time
import pyautogui


play_obj = None
wave_obj = sa.WaveObject.from_wave_file("assets/cash.wav")
detector_on = True
# Get the screen resolution
screen_width, screen_height = pyautogui.size()
WINDOW_BOX = (0, 0, screen_width, screen_height)
print(f"Window size:", WINDOW_BOX)

def convert_HSV(h, s, v):
    """
    Convert HSV values in opencv format
    - normal HSV: 0-360, 0-100, 0-100 format
    - opencv HSV: 0-179, 0-255, 0-255 format
    """
    converted_hsv = [h/2, s*255/100, v*255/100]

    return converted_hsv

def run_rubie_detect(light_red_range, dark_red_range, threshold=15000):
    global detector_on
    with mss() as sct:
        while True:
            # Break 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # Toggle detector
            if cv2.waitKey(1) & 0xFF == ord('t'):
                detector_on = not detector_on
                print("Detector toggled to", detector_on)

            if not detector_on:
                cv2.imshow("mask_screen", np.zeros((540, 960, 3), np.uint8))
                time.sleep(3)
                continue
            
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
            
            ruby_detect = np.sum(result)
            # Check if ruby is detected
            print(f"Ruby..{ruby_detect}")
            if detector_on and ruby_detect > threshold:
                # Play sound
                play_obj = wave_obj.play()
                time.sleep(10000/ruby_detect)  # Wait for 1 second
            


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

    run_rubie_detect(light_red_range=light_red_range, dark_red_range=dark_red_range, threshold=10000)
    