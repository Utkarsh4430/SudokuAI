import cv2
import numpy as np
from matplotlib import pyplot as plt
from keras.models import load_model
model = load_model("./test_model")

def predict(img):
    img = cv2.resize(img,(28,28),interpolation = cv2.INTER_AREA)
    # img = 255.0 - img
    # plt.imshow(img,cmap='gray')
    # plt.show()
    # print(type(img[0][0]))
    img = img.astype(np.float32, copy=False)
    img /= 255.0
    img = img.reshape(1,28,28,1)
    pred = model.predict(img)[0]
    # print(pred)
    pred = int(np.argmax(pred)) + 1
    # print(pred)
    # print()
    return int(pred)

def calc(img):
    length = img.shape[0]
    count = 0
    for i in img:
        for j in i:
            if j == 255:
                count+=1
    return (count*100)/(length*length)

def matrix_generator(img):
    matrix = np.zeros((9,9),dtype = np.int8)
    for i in range(9):
        for j in range(9):
            box = img[100*i:100*(i+1),100*j:100*(j+1)]
            
            x = box[30:70,30:70]
            _ ,x = cv2.threshold(x,100,255,cv2.THRESH_BINARY)
            if(calc(x)<10):
                matrix[i,j] = -1
            else:
                matrix[i,j] = predict(box[10:90,10:90])
            # plt.imshow(x, cmap = 'gray')
            # plt.show()
            # matrix[i,j] = predict(box)
    return matrix