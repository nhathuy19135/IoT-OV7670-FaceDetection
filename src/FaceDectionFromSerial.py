from os import getenv
import serial
import cv2
import numpy as np
import blynklib
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

api_key = getenv("THINGSPEAK_API_KEY")
auth_token = getenv("BLYNK_AUTH_TOKEN")

blynk = blynklib.Blynk(auth_token)

# configure the serial connection
ser = serial.Serial(
    port='COM5',
    baudrate=1000000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)
face_cascade = cv2.CascadeClassifier('src\haarcascade_frontalface_default.xml')

pin = 'v4'

while True:
    # read data from the serial port
    data = ser.read(320 * 240)

    # convert the data to a NumPy array
    image = np.frombuffer(data, dtype=np.uint8)

    # reshape the data into an image
    image = image.reshape((240, 320))
    faces = face_cascade.detectMultiScale(image, 1.3, 5)
    
    # draw rectangles around the faces
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        
    # print the number of faces detected
    num_faces = len(faces)
    print ("Num faces: ", num_faces)   
    
        # Send number of faces to Blynk
    blynk_url = requests.get(f"http://blynk.cloud/external/api/update?token={auth_token}&{pin}={num_faces}", )
    print ("Blynk response: ", blynk_url , blynk_url.text)
        
        # Send number of faces to ThingSpeak
    thingSpeak_url = requests.get(f"https://api.thingspeak.com/update?api_key={api_key}&field1={num_faces}")
    print ("ThingSpeak response: ", thingSpeak_url , thingSpeak_url.text)

    # display the image using OpenCV
    cv2.imshow('Image', image)
    if cv2.waitKey(1) == ord('q'):
        break
