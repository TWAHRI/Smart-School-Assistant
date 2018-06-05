import numpy as np
import app_utils
import re
import sys
import traceback
import pygame
import time
import cv2
from semantic.numbers import NumberService


WORDS = ["CONTACT", "CONTACTS"]

PRIORITY = 0


img = cv2.imread('/home/pi/jasper/static/text/phone1.png')

def image_viewer():
    window_name = 'IMAGE'
    
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, img)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()
    
    
def handle(text, mic, profile, person):
    image_viewer()


def isValid(text):
    return bool(re.search(r'\b(contact|contacts)\b', text, re.IGNORECASE))
