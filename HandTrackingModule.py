# CREATING A MODULE TO TRACK HAND POSITIONS AND MOVEMENTS.

# Import the necessary libraries to open the webcam.
import cv2
import mediapipe as mp
import time


class handDetector:
    def __init__(self, mode=False, maxHands=2, modelCompl=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelCompl = modelCompl
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelCompl, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        # Convert the image to RGB.
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process the image.
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Using mpDraw to draw the points and connections on the hands.
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNumber=0, draw=True):

        landmarkList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]

            for idd, lm in enumerate(myHand.landmark):
                height, width, channels = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                landmarkList.append([idd, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (0, 0, 255), cv2.FILLED)

        return landmarkList

def main():

    prevTime = 0
    cap = cv2.VideoCapture(0)

    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        landmarkList = detector.findPosition(img)
        if len(landmarkList) != 0:
            # Print the position of each one of the 21 landmarks.
            print(landmarkList)
        # Getting the fps and displaying them on the screen.
        curTime = time.time()
        fps = 1 / (curTime - prevTime)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        prevTime = curTime

        cv2.imshow("Image", img)
        # If 'E' is pressed then exit the webcam.
        if cv2.waitKey(1) & 0xFF == ord('E'):
            break


if __name__ == "__main__":
    main()
