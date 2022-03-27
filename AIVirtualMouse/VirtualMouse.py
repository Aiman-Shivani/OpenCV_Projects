import cv2
import time
import numpy as np
import Hand_Tracking_Module as htm
import autopy

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
plocX, plocY = 0,0
clocX,clocY = 0,0
detector = htm.handDetector(maxHands = 1)
wScr, hScr = autopy.screen.size()
frameR = 100
smoothening = 5
while True:
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    #Find Hand Landmarks
    success, img = cap.read()
    # Get the tip of the index and middle fingers
    if(len(lmList)!= 0):
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
    #Check which fingers are up
        fingers = detector.fingersUp()

        #Only index finger = Moving Mode
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        if fingers[1] == 1 and fingers[2] == 0:
            #Convert Cordinates acc to screen
            x3 = np.interp(x1, (frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR,hCam-frameR),(0,hScr))
            #Smoothen Values
            clocX = plocX +(x3-plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            #Mode Mouse
            autopy.mouse.move(wScr-clocX,clocY)
            cv2.circle(img, (x1,y1), 15,(255,0,255), cv2.FILLED)
            plocX,plocY = clocX, clocY
        #Both index and middle = Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # Distance between fingers
            length, img, lineInfo = detector.findDistance(8,12,img)
            print(length)

            # click mouse of dist short
            if length < 40:
                cv2.circle(img, (x1,y1), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.click()




    #Frame Rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0, 3))
    #Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
