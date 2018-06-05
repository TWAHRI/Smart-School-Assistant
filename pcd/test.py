import numpy as np
import cv2
import Face_recognition.face_recognition_classes as Im

Subjects = ["", "Emma Watson", "Daniel Radclif", "Amani Younsi", "Hamdy Twahry"]
Data = Im.Image_Data_Prepare()
Data.prepare_training_data("/home/amani/Documents/pcd/Face_recognition/Data")
print(len(Data.faces), len(Data.labels))
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(Data.faces, np.array(Data.labels))
la = 0

cap = cv2.VideoCapture(0)


while(True):

    ret, frame = cap.read()
    if ret is True:
        # frame = cv2.flip(frame, 1)
        cv2.rectangle(frame, (120, 50), (520, 430), (0, 255, 0), 1, 8, 0)
        cv2.imshow('frame', frame)
        if frame is not None:
            face, rect = Im.Image(frame).detect_face()
            print(face is None)
            if rect is not None:
                (x, y, w, h) = rect
                if x > 120 and y > 50 and x+h < 520 and y+w < 430:
                    print('true')
                    cv2.imwrite('/home/amani/Documents/pcd/Face_recognition/test/test4.png', frame)
                    break
                else:
                    print('false')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

image = cv2.imread('/home/amani/Documents/pcd/Face_recognition/test/test4.png')

bla = Im.Image(image)
la = bla.predict(face_recognizer)
if la > 0 and la < len(Subjects):
    print(Subjects[la])
else:
    print("unkown")
