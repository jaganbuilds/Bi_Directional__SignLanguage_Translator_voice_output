import cv2
import mediapipe
import numpy
import autopy

cap = cv2.VideoCapture(0)
initHand = mediapipe.solutions.hands
mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
draw = mediapipe.solutions.drawing_utils
wScr, hScr = autopy.screen.size()
pX, pY = 0, 0
cX, cY = 0, 0

def handLandmarks(colorImg):
    landmarkList = []
    landmarkPositions = mainHand.process(colorImg)
    landmarkCheck = landmarkPositions.multi_hand_landmarks
    if landmarkCheck:
        for hand in landmarkCheck:
            for index, landmark in enumerate(
                    hand.landmark):
                draw.draw_landmarks(img, hand,
                                    initHand.HAND_CONNECTIONS)
                h, w, c = img.shape
                centerX, centerY = int(landmark.x * w), int(
                    landmark.y * h)
                landmarkList.append([index, centerX, centerY])
    return landmarkList


def fingers(landmarks):
    fingerTips = []
    tipIds = [4, 8, 12, 16, 20]

    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)


    for id in range(1, 5):
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2] : fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips

count = 0
flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0
flag5 = 0


frame_check = 20
while True:
    check, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lmList = handLandmarks(imgRGB)
    #print(lmList)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1:]
        x2, y2 = lmList[12][1:]
        finger = fingers(lmList)
        #print(finger)

        count = finger[0]+finger[1]+finger[2]+finger[3]+finger[4]
        #print(count)

        if(count == 1):
            flag1 += 1
            if flag1 >= frame_check:
                print(1)
                flag1 = 0
        else:
            flag1 = 0

        if (count == 2):
            flag2 += 1
            if flag2 >= frame_check:
                print(2)
                flag2 = 0
        else:
            flag2 = 0

        if (count == 3):
            flag3 += 1
            if flag3 >= frame_check:
                print(3)
                flag3 = 0
        else:
            flag3 = 0

        if (count == 4):
            flag4 += 1
            if flag4 >= frame_check:
                print(4)
                flag4 = 0
        else:
            flag4 = 0

        if (count == 5):
            flag5 += 1
            if flag5 >= frame_check:
                print(5)
                flag5 = 0
        else:
            flag5 = 0




    cv2.putText(img, "****************ALERT!****************"+str(count), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
