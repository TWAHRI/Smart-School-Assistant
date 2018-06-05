import numpy as np
import cv2
import face_recognition_classes as Im
import jasperpath
import modules.Models_classes as Mo

Subjects = [""]
Person = None
count_poss = 3
data = Mo.data
conn = data.engine.connect()
stud = data.session.query(Mo.Person).all()
for s in stud:
    Subjects.append(s.name)
    
print(Subjects)
Data = Im.Image_Data_Prepare()
Data.prepare_training_data("/home/pi/jasper/client/Data")

def trait(cnt, face_recognizer, la, mic):
    print("xxxxxx", la)
    image = cv2.imread('/home/pi/jasper/client/test/test4.png')
    test = False
    bla = Im.Image(image)
    la = bla.predict(face_recognizer)
    print(la)
    print(cnt)
    global Subjects
    if la > 0 and la < len(Subjects) and (cnt >= 0):
        global Person
        Person = data.session.query(Mo.Person).filter(Mo.Person.person_id == la).first()
        print(Person)
        print(Subjects[la])
        test = True
        name = Subjects[la]
        mic.say("Hello" + name)
        mic.authentication_modify(True)
    elif cnt >= 0 and (la >= len(Subjects) or la <= 0):
        mic.say("sorry! I did not recognize you. try to fixe your face in the center of the frame")
        global Person
        Person = None
    elif cnt < 0:
        mic.say("sorry! I could not identify you")
        mic.authentication_modify(False)
        global Person
        Person = None
    return test


class Authentication: 
    def __init__(self, l, mic):
        self.la = l
        self.mic = mic
    
    def Person_ret(self):
        return(Person)
        
    def authenticate(self):            
        print(len(Data.faces), len(Data.labels))
        face_recognizer = cv2.face.createLBPHFaceRecognizer()
        global Data
        face_recognizer.train(Data.faces, np.array(Data.labels))
        global count_poss
        cap = cv2.VideoCapture(0)
        test = False

        while(True):

            ret, frame = cap.read()
            window_name = 'Authentication'
            if ret is True:
                # frame = cv2.flip(frame, 1)
                cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)   
                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.rectangle(frame, (120, 50), (520, 430), (0, 255, 0), 1, 8, 0)
                cv2.imshow(window_name, frame)
                if frame is not None:
                    face, rect = Im.Image(frame).detect_face()
                    print(face is None)
                    if rect is not None:
                        (x, y, w, h) = rect
                        if x > 120 and y > 50 and x+h < 520 and y+w < 430:
                            print('true')
                            cv2.imwrite('/home/pi/jasper/client/test/test4.png', frame)
                            count_poss = count_poss - 1
                            test = trait(count_poss, face_recognizer, self.la, self.mic)
                        else:
                            print('false')
            if count_poss < 0 or test is True:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()



