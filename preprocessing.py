import cv2
import matplotlib.pyplot as plt
import numpy as np

def filters(img,thickness):
    image = cv2.resize(img.copy(), (1200, 900), interpolation=cv2.INTER_AREA)
    image = cv2.GaussianBlur(image.copy(), (9, 9), 0)
    thresh_hold = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)
    inverted = cv2.bitwise_not(thresh_hold, thresh_hold)
    kernel = np.ones(thickness, np.uint8)
    inverted = cv2.dilate(inverted, kernel)
    return inverted

def four_point_transform(image,tl,tr,br,bl):
    rect = np.array([tl,tr,br,bl],dtype = "float32")
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def preprocess(img,dimension):
    inverted = filters(img,(3,3))

    contours, _ = cv2.findContours(inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    quadrangle = contours
    evals = np.zeros([3, len(quadrangle)])
    
    for index, coordinates in enumerate(quadrangle):
        coordinates = coordinates[0]
        evals[0, index] = sum(coordinates)
        evals[1, index] = coordinates[0] - coordinates[1]
        evals[2, index] = coordinates[1] - coordinates[0]
    upper_left = quadrangle[np.argmin(evals, axis=1)[0]][0]
    lower_right = quadrangle[np.argmax(evals, axis=1)[0]][0]
    upper_right = quadrangle[np.argmax(evals, axis=1)[1]][0]
    lower_left = quadrangle[np.argmax(evals, axis=1)[2]][0]
    # print( np.array([upper_left, upper_right, lower_right, lower_left]))
    # print(bounding_rect.shape)

    # img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
    img = filters(img,(1,1))
    warped = four_point_transform(img,upper_left,upper_right,lower_right,lower_left)
    plt.imshow(warped)
    plt.show()



