import face_recognition
import cv2
import numpy as np
import os
import time
from threading import Thread
from PyQt5.QtCore import *

registered_faces_encodings = []
registered_faces_names = []

class Communicate(QObject):
    new_image = pyqtSignal(str)

class Face_Recognizer:
    def __init__(self, camera_id = -1):
        self.camera_id = camera_id
        self.im_s = Communicate()
        self.is_running = False

    #This function will take a sample frame
    #save the picture of the given user in a folder
    #returns the path of the saved image
    def saveFaceImage(self, face_name='user'):
        self.face_name = face_name
        self.base_path = os.path.join(os.getcwd(), 'Users')
        if not os.path.isdir(self.base_path):
            os.makedirs(self.base_path)

        camera = cv2.VideoCapture(self.camera_id)
        if not camera.isOpened():
            raise (ValueError("Please make sure you entered a correct camera index"))

        while camera.isOpened():
            is_valid, frame = camera.read()
            if is_valid:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                #self.rgb_small_frame = small_frame[:, :, ::-1]
                self.rgb_small_frame = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)

                self.file_name = '{}.png'.format(self.face_name)
                self.file_path = os.path.join(self.base_path, self.file_name)
                try:
                    cv2.imwrite(str(self.file_path), self.rgb_small_frame)
                    time.sleep(1)
                    break
                except:
                    print("Can't Save File")

        camera.release()
        return self.file_path

    #find the face in the saved picture
    #store the encodings of the face
    #store it's name and encodings
    def registerFace(self, face_name, face_image_path):
        registered = False
        self.face_image_path = face_image_path
        self.face_location = []
        self.face_encoding = []
        self.face_name = face_name

        self.user_image = face_recognition.load_image_file(self.face_image_path)

        if not registered:
            try:
                self.face_encoding = face_recognition.face_encodings(self.user_image)[0]
                registered_faces_encodings.append(self.face_encoding)
                registered_faces_names.append(self.face_name)
            except:
                print("No face found in the image")
                return 'failed'

            print(registered_faces_names)
            return 'success'

    def compareToDatabase(self, unknown_face_encoding=None):
        if not self.is_running:
            self.is_running = True
            self.m_thread = Thread(target= self._compareToDatabase )
            self.m_thread.start()

    def _compareToDatabase(self):
        authenticated = False
        video_capture = cv2.VideoCapture(0)
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while not authenticated:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(registered_faces_encodings, face_encoding)
                    name = "Unknown"
                    face_distances = face_recognition.face_distance(registered_faces_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = registered_faces_names[best_match_index]
                        #authenticated = True
                    registered_faces_names.append(name)

            #process_this_frame = not process_this_frame
            for (top, right, bottom, left), name in zip(face_locations, registered_faces_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                cv2.imwrite(".tmp.png" , frame)
                self.im_s.new_image.emit(".tmp.png")
                # Display the resulting image
            #cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!


        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    def removeFaceData(self, face_name):
        pass

'''
recognizer = Face_Recognizer()
recognizer.registerFace()
recognizer.saveFaceImage('Kareem')
'''

