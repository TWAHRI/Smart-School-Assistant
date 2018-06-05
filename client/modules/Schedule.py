import numpy as np
import app_utils
import re
import sys
import traceback
import pygame
import time
import cv2
from semantic.numbers import NumberService
from sqlalchemy.orm import joinedload
import Models_classes as Mo

WORDS = ["SCHEDULE"]

PRIORITY = 0

def image_viewer(person): 
    data = Mo.data
    window_name = 'IMAGE'
    type = person.discriminator
    if type == 'professor':
        path = person.emploi_path
    elif type == 'student':
        cl = data.session.query(Mo.Class).options(joinedload(Mo.Class.students)).filter(Mo.Student.person_id == person.person_id).first()
        path = cl.emploi_path        
    img = cv2.imread(path)
    
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, img)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()
    
def handle(text, mic, profile, person):
    print("schedule")
    pygame.init()
    pygame.mixer.music.load("/home/pi/jasper/static/audio/beep_hi.wav")
    pygame.mixer.music.play()
    time.sleep(0.2)
    
    image_viewer(person)
    time.sleep(0.2)
    
    pygame.mixer.music.load("/home/pi/jasper/static/audio/beep_lo.wav")
    pygame.mixer.music.play()
    

def isValid(text):
    return bool(re.search(r'\b(schedule)\b', text, re.IGNORECASE))
