import cv2
import matplotlib.pyplot as plt
import os
from preprocessing import preprocess
from matrix_gen import matrix_generator
from solver import solve
import sys

image_path = ''
fn = sys.argv[1]
if os.path.exists(fn):
    image_path = fn

    SQUARE_IMG_DIM = (81,81)

    img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    img = preprocess(img,SQUARE_IMG_DIM)
    img = cv2.resize(img,(900,900),interpolation=cv2.INTER_AREA)
    # plt.imshow(img)
    # plt.show()
    matrix = matrix_generator(img)
    print("Given Sudoku:")
    for i in range(12):
        print(" -",end="")
    print()
    for i in range(9):
        print("| ",end="")
        for j in range(9):
            if(matrix[i][j]==-1):
                print("  ",end = "")
            else:
                print(matrix[i][j],end = ' ')
            if (j+1)%3==0 and j!=8:
                print('| ',end ="")
        print("|")
        if (i+1)%3==0:
            for i in range(12):
                print(" -",end="")
            print()
    print('Solved Sudoku:')

    solution,possible = solve(matrix,0,0,9)
    if possible:
        for i in range(12):
            print(" -",end="")
        print()
        for i in range(9):
            print("| ",end="")
            for j in range(9):
                print(solution[i][j],end = ' ')
                if (j+1)%3==0 and j!=8:
                    print('| ',end ="")
            print("|")
            if (i+1)%3==0:
                for i in range(12):
                    print(" -",end="")
                print()
    else:
        print("No solution was found")
else:
    print("Incorrect Path!")