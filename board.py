import cv2
import numpy as np

cap = cv2.VideoCapture(0)
frameWidth = 1920
frameHeight = 1080
cap.set(3, frameHeight)
cap.set(4, frameWidth)
#cap.set(10, 150)

myColors = [
    [23, 91, 120, 96, 255, 255]#yellow pointer
    #highliter[21, 56, 112, 37, 255, 255]
    #[103, 124, 84, 117, 207, 255],
    #[15, 134, 51, 85, 248, 255],
    ]

myColorValues = [
    [255, 0, 0],
    #[255, 255, 0]
]

myPoints = [] #x,y,ColorID

def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        # cv2.imshow("HSV", imgHSV)
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]), mask)
    return newPoints

myPoints = []


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 100:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img1 = cap.read()
    img = cv2.flip(img1, +1)
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints)!=0:
        for newPoint in newPoints:
            myPoints.append(newPoint)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints, myColorValues)
    # cv2.imshow("Video", img)
    cv2.imshow("Res", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
