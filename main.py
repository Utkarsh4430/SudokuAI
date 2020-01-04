import cv2
import matplotlib.pyplot as plt
import os
from preprocessing import preprocess

image_path = './a.jpg'
SQUARE_IMG_DIM = (81,81)
img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
img = preprocess(img,SQUARE_IMG_DIM)


