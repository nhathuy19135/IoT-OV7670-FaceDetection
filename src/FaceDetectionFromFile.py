# This code read new images continuously from a folder, and use that images to detect faces. You will need to setup the output folder in ArduinoImageCapture for the code to work. 
import cv2
import os
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
api_key = os.getenv("THINGSPEAK_API_KEY")
auth_token = os.getenv("BLYNK_AUTH_TOKEN")

path = r'D:\uni22\IoT\imageTest' # path to the folder with images

stop_key = ord('q') # wait for 'q' key to be pressed

last_time = time.time() # time of the last image
# Load the cascade for face detection
face_cascade = cv2.CascadeClassifier('src\haarcascade_frontalface_default.xml')

while True:
    # Check if there are new images in the folder
    for filename in os.listdir(path):
        if os.path.getmtime(os.path.join(path, filename)) > last_time:
            img = cv2.imread(os.path.join(path, filename))
            # Load the image for face detection
            faces = face_cascade.detectMultiScale(img, 1.3, 5)
            # Draw rectangles around the faces
            for (x,y,w,h) in faces:
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            # Display the image
            cv2.imshow('ImageWindow', img)
            last_time = time.time()
            # count the number of faces
            num_faces = len(faces)
            print ("Num faces: ", num_faces)
            
        # Check if the user wants to stop the program
        if cv2.waitKey(1) & 0xFF == stop_key:
            break
    else:
        continue
    break