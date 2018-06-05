import screeninfo
import numpy as np
import re
import sys
import traceback
import pygame
import time
import cv2
from semantic.numbers import NumberService


def image_viewer(img):
    window_name = 'Schedule'
    
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, img)
    cv2.waitKey(7000)
    cv2.destroyAllWindows()

