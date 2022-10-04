import numpy as np
import cv2

cap = cv2.VideoCapture(r'C:\Users\adhem\Desktop\Python\DroneLoad\VF.mp4')#
while(1):
  ret, frame = cap.read()
  print(frame)
  rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  cv2.imshow('tessst', frame)
  key = cv2.waitKey(1)
  if key == ord(' '):
    break

cap.release()
cv2.destroyAllWindows()