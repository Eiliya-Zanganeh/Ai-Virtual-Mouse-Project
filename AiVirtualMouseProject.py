import math

import numpy as np, cv2, time
from Modules.HandTracking import handTrackingModule as htm
import pyautogui

wScreen, hScreen = pyautogui.size()
# print(wScreen, hScreen)
wCam, hCam = 640, 480
frameR = 100
smoothening = 5

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
plocx, plocy = 0, 0
clocx, clocy = 0, 0
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    hands = detector.findPosition(img, draw=False)

    if len(hands) != 0:
        x1, y1 = hands[0][1][8][1:]
        x2, y2 = hands[0][1][12][1:]

        fig = detector.fingersUp(img, hand_custome=hands[0])
        # print(fig)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (0, 0, 255), 2)
        if fig[1][0][1][1] == 1 and fig[1][0][1][2] == 1:
            print('Select')
            cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)

            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            length = math.hypot(x2 - x1, y2 - y1)
            if length < 40:
                cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
                pyautogui.click()



        elif fig[1][0][1][1] == 1 and fig[1][0][1][2] == 0:
            print('Move')
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScreen))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScreen))

            clocx = plocx + (x3 - plocx) / smoothening
            clocy = plocy + (x3 - plocy) / smoothening

            pyautogui.moveTo(x3, y3)

            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            plocx, plocy = clocx, clocy



        

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('img', img)
    cv2.waitKey(1)