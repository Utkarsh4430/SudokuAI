import numpy as np
import math

def canplace(matrix,i,j,n,num):
    for x in range(9):
        if matrix[i][x]==num or matrix[x][j]==num:
            return False
    n = int(math.sqrt(n))
    sx = int((i//n)*n)
    sy = int((j//n)*n)

    for x in range(sx,sx+n):
        for y in range(sy,sy+n):
            if(matrix[x][y]==num):
                return False
    return True

def solve(matrix,i,j,n):
    if i==n:
        return matrix,True
    if j==n:
        # print(1)
        return solve(matrix,i+1,0,n)
    if matrix[i][j]!=-1:
        return solve(matrix,i,j+1,n)
    # print(matrix[i][j])
    for num in range(1,10):
        if canplace(matrix,i,j,n,num):
            matrix[i][j]= num
            matrix2,possible = solve(matrix,i,j+1,n)
            if possible:
                return matrix2,True
    matrix[i][j] = -1
    return matrix, False

    