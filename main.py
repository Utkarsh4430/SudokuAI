import cv2
import matplotlib.pyplot as plt
import os
from preprocessing import preprocess
from matrix_gen import matrix_generator

image_path = './image.jpg'
SQUARE_IMG_DIM = (81,81)
img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
img = preprocess(img,SQUARE_IMG_DIM)
img = cv2.resize(img,(900,900),interpolation=cv2.INTER_AREA)
# plt.imshow(img,cmap='gray')
# plt.show()
matrix = matrix_generator(img)
for i in range(9):
    for j in range(9):
        if(matrix[i][j]==-1):
            print(". ",end = "")
            continue
        print(matrix[i][j],end = ' ')
    print()
