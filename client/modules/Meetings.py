import app_utils
import re
import pygame
import time
from semantic.numbers import NumberService
from sqlalchemy.orm import joinedload
import Models_classes as Mo

WORDS = ["MEETINGS", "MEET"]

PRIORITY = 0


def handle(text, mic, profile, person):
    pygame.init()
    pygame.mixer.music.load("/home/pi/jasper/static/audio/beep_hi.wav")
    pygame.mixer.music.play()
    time.sleep(0.2)
    
    type = person.discriminator
    if type == 'professor':
        re = Mo.data.session.query(Mo.Reunion).options(joinedload(Mo.Reunion.professors)).filter(Mo.Professor.person_id == person.person_id).all()
        if re is not None:
            mic.say('you have the following meetings')
            for met in re:
                name = str(met.name)
                date = str(met.date)
                mic.say('the ' + name + 'on ' + date)
        else:
            mic.say('you have no meetings')
    elif type == 'student':
        mic.say('Sorry yo dont have the privilege to access meetings')
     
    pygame.mixer.music.load("/home/pi/jasper/static/audio/beep_lo.wav")
    pygame.mixer.music.play()
    time.sleep(0.2)
        
def isValid(text):
    return bool(re.search(r'\b(meetings|meet)\b', text, re.IGNORECASE))


