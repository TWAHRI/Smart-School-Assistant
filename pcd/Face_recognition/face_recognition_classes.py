import os
import cv2
import numpy as np


def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)


class Image:
    def __init__(self, img):
        self.image = img

    def detect_face(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('/home/amani/Documents/opencv/data/lbpcascades/lbpcascade_frontalface.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)
        if (len(faces) == 0):
            print(1)
            return None, None

        (x, y, w, h) = faces[0]
        return gray[y:y+w, x:x+h], faces[0]

    def predict(self, face_recognizer):
        img = Image(self.image)
        face, rect = img.detect_face()
        if face is not None:
            lab, confidence = face_recognizer.predict(face)

            if confidence < 60:
                label = lab
            else:
                label = 0

        return label


class Image_Data_Prepare:
    __image_Data = None
    faces = []
    labels = []

    def __new__(cls):
        if Image_Data_Prepare.__image_Data is None:
            Image_Data_Prepare.__image_Data = object.__new__(cls)
        return Image_Data_Prepare.__image_Data

    def prepare_training_data(self, data_folder_path):
        dirs = os.listdir(data_folder_path)
        for dir_name in dirs:
            if not dir_name.startswith("s"):
                continue
            label = int(dir_name.replace("s", ""))
            subject_dir_path = data_folder_path + "/" + dir_name
            subject_images_names = os.listdir(subject_dir_path)
            for image_name in subject_images_names:
                if image_name.startswith("."):
                    continue
                image_path = subject_dir_path + "/" + image_name
                image = cv2.imread(image_path)
                img = Image(image)
                face, rect = img.detect_face()
                if face is not None:
                    self.faces.append(face)
                    self.labels.append(label)
