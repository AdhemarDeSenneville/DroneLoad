import numpy as np
import cv2
import time

cap = cv2.VideoCapture(r'C:\Users\adhem\Desktop\Python\DroneLoad\VF.mp4')
#cap = cv2.VideoCapture(0)

#HyperParametres
Xf = 10
Yf = 10
Wf = 10
Hf = 10
XYWHTime=time.time()

Bound=10
RatioCarre=1.5
RatioAir=0.3

#
#    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2)
def getContours(img):

    #Paramètres
    Minim=0
    global Xf
    global Yf
    global Wf
    global Hf
    global XYWHTime
    if time.time()-XYWHTime>3:
        Xf=10
        Yf=10
        Wf=10
        Hf=10
    
    areaMin = 5000 #cv2.getTrackbarPos("Area", "Parameters")
    areaMax = 120000

    #Préprocéssing
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #converte
    np_dilatatation = cv2.GaussianBlur(imgGray, (7, 7), 0) #Flou
    np_dilatatation = cv2.Canny(np_dilatatation, 0, 80) #dila
    mat = np.ones((3,3),np.uint8)
    np_dilatatation = cv2.dilate(np_dilatatation,mat,iterations=1) #dilatation

    #Contours
    contours, hierarchy = cv2.findContours(np_dilatatation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(len(contours))
        if area > areaMin and area < areaMax:
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
            #print(area/(h*w),area,"  et ",w*h)
            if  1/RatioCarre<w/h<RatioCarre and RatioAir<area/(h*w) and w*h<100000: #y>Bound and x>Bound and x+w<img.shape[1]-Bound and y+h<img.shape[0]-Bound and
                if area/(h*w)>Minim:
                    Minim=area/(h*w)
                    Xf=x
                    Yf=y
                    Wf=w
                    Hf=h
                    XYWHTime=time.time()



while True:
    ret, frames = cap.read()
    
    getContours(frames)

    np_img2 = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)

    cv2.rectangle(np_img2, (Xf, Yf), (Xf + Wf, Yf + Hf), (0, 255, 0), 5)
    cv2.putText(np_img2, "Window: " + str(int(0)), (Xf + Wf + 20, Yf + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,(0, 255, 0), 2)

    cv2.imshow('tesst', np_img2)
    key = cv2.waitKey(20)
    if key == ord(' '):
        break

