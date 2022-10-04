import numpy as np
import cv2
import time

Bound=10
RatioCarre=1.5
RatioAir=0.3

cap = cv2.VideoCapture(r'C:\Users\adhem\Desktop\Python\DroneLoad\VF.mp4')
#cap = cv2.VideoCapture(0)

def empty(a):
    pass

#cv2.namedWindow("Parameters")
#cv2.resizeWindow("Parameters",640,240)
#cv2.createTrackbar("Threshold1","Parameters",0,255,empty)
#cv2.createTrackbar("Threshold2","Parameters",80,255,empty)
#cv2.createTrackbar("Area","Parameters",5000,30000,empty)

Xf = 20
Yf = 20
Wf = 20
Hf = 20
XYWHTime=time.time()

#
#    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2)
def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
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

    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(len(contours))
        areaMin = 5000 #cv2.getTrackbarPos("Area", "Parameters")
        areaMax = 120000
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

    cv2.rectangle(imgContour, (Xf, Yf), (Xf + Wf, Yf + Hf), (0, 255, 0), 5)
    cv2.putText(imgContour, "Window: " + str(int(Minim)), (Xf + Wf + 20, Yf + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,(0, 255, 0), 2)



while True:
    ret, frames = cap.read()
    
    #if frames==None:
     #   break
    #vis2 = cv2.cvtColor(np_image, cv2.COLOR_GRAY2BGR)
    #print(type(np.max(vis2)), "vis2")
    #print(np.max(vis2))
    imgGray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    #imgGray = frames
    #np_img2 = np.uint8(imgGray)
    #print(type(np.max(np_img2)), "np_img2")
    #print(np.max(np_img2))
    np_img2 = imgGray
    np_dilatatation = cv2.GaussianBlur(np_img2, (7, 7), 0) #Flou

    threshold1 = 0 #cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = 80 #cv2.getTrackbarPos("Threshold2", "Parameters")
    np_dilatatation = cv2.Canny(np_dilatatation, threshold1, threshold2) #dila

    mat = np.ones((3,3),np.uint8)

    np_dilatatation = cv2.dilate(np_dilatatation,mat,iterations=1) #dilatation 

    getContours(np_dilatatation,np_img2)
    #np_canny = cv2.
    # np_image : unit16


    #print(np.max(np_image))
    #print(type(np.max(np_image)))


    #cv2.imshow('test', np.uint16(imgGray)*5)

    cv2.imshow('tessst', np_dilatatation)
    cv2.imshow('tesst', np_img2)
    key = cv2.waitKey(20)
    if key == ord(' '):
        break


'''
try:
    while True:
        # Create a pipeline object. This object configures the streaming camera and owns it's handle
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth: continue

        # Print a simple text-based representation of the image, by breaking it into 10x20 pixel regions and approximating the coverage of pixels within one meter
        coverage = [0]*64
        for y in range(480):
            for x in range(640):
                dist = depth.get_distance(x, y)
                if 0 < dist and dist < 1:
                    coverage[x//10] += 1

            if y%20 is 19:
                line = ""
                for c in coverage:
                    line += " .:nhBXWW"[c//25]
                coverage = [0]*64
                print(line)

finally:
    pipeline.stop()
'''
