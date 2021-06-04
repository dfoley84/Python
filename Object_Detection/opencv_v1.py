#!/usr/bin/python3
import numpy as np
import cv2
function_person = False
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
Camera = 'http://:8081)'
cap = cv2.VideoCapture(Camera)
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        if not function_person:
            print('Hello')
            function_person = True
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
