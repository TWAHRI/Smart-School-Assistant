import app_utils
import re
import pygame
import time
from semantic.numbers import NumberService

WORDS = ["CATCH"]

PRIORITY = 0

filename = '/home/pi/jasper/static/text/chatch-up.txt'

def getMarks(filename):
    pygame.init()
    pygame.mixer.music.load("/home/pi/jasper/static/audio/beep_hi.wav")
    pygame.mixer.music.play()
    time.sleep(0.5)
    
    marksFile = open(filename)
    marks = marksFile.read()
    print(marks)
    return marks


def handle(text, mic, profile, person):
    marks = getMarks(filename)
    mic.say(marks)
    mic.say("All set")
    time.sleep(0.5)
    pygame.mixer.music.load("/home/pi/jasper/static/audio/beep_lo.wav")
    pygame.mixer.music.play()
    time.sleep(0.2)

def isValid(text):
    return bool(re.search(r'\b(catch)\b', text, re.IGNORECASE))

