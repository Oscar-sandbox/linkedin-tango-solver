# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 21:49:38 2025
@author: oscar
"""
from collections import defaultdict
import numpy as np
import cv2

def parse_tango_img(img):
    ''' Parses an image representation of a board into an NxN numpy array and 
    a dictionary of markings.'''
    img = img.copy()
    N = 6
    
    # Crop the image to isolate the board. 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)
    x, y, dx, dy = cv2.boundingRect(contour)
    
    assert 0.95 < dy/dx < 1.05, 'Could not detect square board'  
    img = img[y:y+min(dx,dy), x:x+min(dx,dy)]
    d = len(img) // N  # cell width. 
    
    # Detect suns and moons based on HSV hue. 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_Y = cv2.inRange(hsv, (0, 100, 100), (30, 255, 255)) # yellow.
    hsv_B = cv2.inRange(hsv, (90, 100, 100), (120, 255, 255)) # blue.
    board = np.zeros((N, N), dtype=int)
    
    for i in range(N):
        for j in range(N):
            if np.any(hsv_Y[i*d:(i+1)*d, j*d:(j+1)*d]): board[i,j] = +1    
            if np.any(hsv_B[i*d:(i+1)*d, j*d:(j+1)*d]): board[i,j] = -1
    
    # Detect '=' and 'x' markings based on connected components.             
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    marks = defaultdict(list)
    dd = d // 8  # marking half width. 
    
    for k in range(N):
        for l in range(N-1):
            hy, hx = int((k+0.5)*d), (l+1)*d
            mark = binary[hy-dd:hy+dd, hx-dd:hx+dd]
            retval, _ = cv2.connectedComponents(mark)
            
            if retval in {2,3}:
                sign = 1 if retval == 3 else -1 
                marks[(k,l)].append(((k,l+1), sign))
                marks[(k,l+1)].append(((k,l), sign))
                
            hy, hx = (l+1)*d, int((k+0.5)*d), 
            mark = binary[hy-dd:hy+dd, hx-dd:hx+dd]
            retval, _ = cv2.connectedComponents(mark)
            
            if retval in {2,3}:
                sign = 1 if retval == 3 else -1
                marks[(l,k)].append(((l+1,k), sign))
                marks[(l+1,k)].append(((l,k), sign))
                
    return board, marks, img

def draw_tango_board(img, board, original_board):
    ''' Draws the solution of the puzzle on top of an image.'''
    img = img.copy()
    N = 6
    
    d = len(img) // N    
    color_in = {1: (35,166,245), -1: (216,124,71)}
    color_out = {1: (0,101,186), -1: (114,66,53)}
    
    for i in range(N):
        for j in range(N):
            if original_board[i,j]: continue
            hy, hx = int((j+0.5)*d), int((i+0.5)*d)
            cv2.circle(img, (hy, hx), d//5, color_in[board[i,j]], -1, cv2.LINE_AA)
            cv2.circle(img, (hy, hx), d//5, color_out[board[i,j]], 1, cv2.LINE_AA)
 
    return img 
    
    

    
    


