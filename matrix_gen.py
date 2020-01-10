import cv2
import numpy as np
from matplotlib import pyplot as plt
from keras.models import load_model
model = load_model("./test_model")

def centering_number(box,visited):
    up = down = left = right = -1
    for i in range(visited.shape[0]):
        for j in visited[i]:
            if(j==1):
                up = i
                break
        if not up==-1:
            break
    for i in range(visited.shape[0]-1,-1,-1):
        for j in visited[i]:
            if j==1:
                down = i
                break
        if not down==-1:
            break
    for i in range(visited.shape[1]):
        for j in visited[:,i]:
            if(j==1):
                left = i
                break
        if not left==-1:
            break
    for i in range(visited.shape[1]-1,-1,-1):
        for j in visited[:,i]:
            if j==1:
                right = i
                break
        if not right==-1:
            break
    width = right-left
    height = down-up
    new_box = np.zeros(box.shape)
    new_box[(box.shape[0]-height)//2:(box.shape[0]-height)//2 + height, (box.shape[1]-width)//2:(box.shape[1]-width)//2 + width] = box[up:down,left:right]
    return new_box        

def connected_comp(box,visited,i,j):
    if box[i][j]==0 or visited[i][j]==1:
        return visited
    visited[i][j] = 1
    visited = connected_comp(box,visited,i,j+1)
    visited = connected_comp(box,visited,i,j-1)
    visited = connected_comp(box,visited,i-1,j)
    visited = connected_comp(box,visited,i+1,j)
    return visited

def removing_boundary(box):
    visited = np.zeros(box.shape)
    for i in range(30,70):
        for j in range(30,70):
            if(visited[i][j]):
                continue
            if box[i][j]==0:
                continue
            else:
                visited = connected_comp(box,visited,i,j)
    for i in range(box.shape[0]):
        for j in range(box.shape[1]):
            if not visited[i][j]:
                box[i][j] = 0
    return box,visited
    

def predict(img):
    img = cv2.resize(img,(28,28),interpolation = cv2.INTER_AREA)
    # img = 255.0 - img
    img = cv2.GaussianBlur(img.copy(), (1,1), 0)
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
                # plt.imshow(box)
                # plt.show()
                improved_box,visited = removing_boundary(box)
                centered_box = centering_number(improved_box,visited)
                matrix[i,j] = predict(centered_box[10:90,10:90])
                # plt.imshow(centered_box)
                # plt.show()
            # plt.imshow(x, cmap = 'gray')
            # plt.show()
            # matrix[i,j] = predict(box)
    return matrix