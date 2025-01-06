# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 02:20:50 2025
@author: oscar
"""
from pathlib import Path
import cv2 

from tango_solver import TangoSolver
from tango_parser import parse_tango_img, draw_tango_board

for f in Path('examples', 'inputs').glob('*'):
    img = cv2.imread(f)
    
    original_board, marks, img = parse_tango_img(img)   
    B = TangoSolver(depth=2).solve(original_board, marks)
    answer = draw_tango_board(img, B, original_board)
    
    answer_filepath = Path('examples', 'outputs', f'answer_{f.name}')
    cv2.imwrite(answer_filepath, answer)
