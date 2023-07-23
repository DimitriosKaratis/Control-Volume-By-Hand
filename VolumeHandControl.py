# CONTROLLING PC'S VOLUME USING HAND GESTURES VIA THE HELP OF PYCAW PACKAGE.

# Importing the necessary libraries.
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Creating a new video capture.
cap = cv2.VideoCapture(0)

# Setting the dimensions of the webcam window.
camWidth, camHeight = 640, 480
cap.set(3, camHeight)
cap.set(4, camHeight)

# Using the module that we previously created in order to track hand movements
# with detection confidence manually set at 70%.
detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPercentage = 0
pTime = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    landmarkList = detector.findPosition(img)
    if len(landmarkList) != 0:
        # Print only the positions of the tip of the thumb (landmark 4) and index fingers (landmark 8).
        # print(landmarkList[4], landmarkList[8])

        # Storing the thumb and index fingers locations at (x1, y1) and (x2, y2) sets of variables respectively.
        x1, y1 = landmarkList[4][1], landmarkList[4][2]
        x2, y2 = landmarkList[8][1], landmarkList[8][2]
        # Storing the location of the midpoint in variables cx and cy.
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Creating three black circles to pinpoint the locations that we care about.
        cv2.circle(img, (x1, y1), 10, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 9, (0, 0, 0), cv2.FILLED)
        # Creating a line connecting the thumb and the index finger.
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 3)

        # The length of the line that we created.
        length = math.hypot(x2 - x1, y2 - y1)

        # Hand range: [40 , 300].
        # Volume range: [-65 , 0].

        # Using numpy package to convert hand range to volume range (vol), volume of the bar (volBar),
        # that we are going to create shortly, and volume percentage (volPercentage).
        vol = np.interp(length, [40, 300], [minVol, maxVol])
        volBar = np.interp(length, [40, 300], [400, 150])
        volPercentage = np.interp(length, [40, 300], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        print(int(length), vol)

        # If the two fingers are touching or if they are close enough, then make the midpoint of the line blue.
        if length < 40:
            cv2.circle(img, (cx, cy), 9, (255, 0, 0), cv2.FILLED)

    # Creating a rectangular bar that fills up when then volume is increased.
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    # Displaying the percentage of the volume on the webcam window.
    cv2.putText(img, f' {int(volPercentage)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # Computing the fps.
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Displaying the fps on the webcam window.
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    # If 'E' (capital) is pressed then exit the webcam.
    if cv2.waitKey(1) & 0xFF == ord('E'):
        break
