# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 01:03:43 2025
@author: oscar
"""
from collections import defaultdict
from copy import deepcopy
import numpy as np

class TangoSolver: 
    def __init__(self, depth): 
        ''' Construct a Tango solver using backtracking.'''
        self.depth = depth     
        
        self.N = 6 # number of rows and columns. 
        self.B = np.zeros((self.N, self.N), dtype=int) # board representation. 
        self.marks = defaultdict(list) # '=' and 'x' markings. 
    
    def check_progress(self):
        ''' Check if self.B has any immediate contradictions.'''
        
        # Check no row or column has more than N/2 suns or moons. 
        if np.any(np.count_nonzero(self.B == +1, 0) > self.N // 2): return False
        if np.any(np.count_nonzero(self.B == -1, 0) > self.N // 2): return False
        if np.any(np.count_nonzero(self.B == +1, 1) > self.N // 2): return False
        if np.any(np.count_nonzero(self.B == -1, 1) > self.N // 2): return False
        
        # Check no row or column has three consecutive suns or moons. 
        for k in range(self.N):
            for l in range(self.N-2):
                if np.all(self.B[k,l:l+3] == +1): return False
                if np.all(self.B[k,l:l+3] == -1): return False
                if np.all(self.B[l:l+3,k] == +1): return False
                if np.all(self.B[l:l+3,k] == -1): return False
        
        # Check all marks "=" and "x" are fulfilled. 
        for (i,j), neighbors in self.marks.items():
            for (i1,j1), sign in neighbors: 
                if self.B[i,j] != sign*self.B[i1,j1]: return False
        
        return True
        
    def check_answer(self): 
        ''' Check if self.B is an answer for the puzzle.'''
        return (np.count_nonzero(self.B) == self.N**2) and self.check_progress()
    
    def fill_trivials(self):     
        '''Recursively fill every trivial position for a sun or a moon.'''
        
        for i in range(self.N):
            for j in range(self.N): 
                if self.B[i,j]: continue
                
                # Fill marks.
                if (i,j) in self.marks.keys():
                    for (i1,j1), sign in self.marks[(i,j)]:
                        if self.B[i1,j1]: 
                            self.B[i,j] = sign * self.B[i1,j1] 
                            self.fill_trivials()
                
                # Fill sequences of 3 symbols. 
                u = self.B[i-1,j] if i > 0 else None
                uu = self.B[i-2,j] if i > 1 else None
                d = self.B[i+1,j] if i < self.N-1 else None
                dd = self.B[i+2,j] if i < self.N-2 else None
                l = self.B[i,j-1] if j > 0 else None
                ll = self.B[i,j-2] if j > 1 else None
                r = self.B[i,j+1] if j < self.N-1 else None
                rr = self.B[i,j+2] if j < self.N-2 else None
                
                if uu and u == uu: 
                    self.B[i,j] = -u
                    self.fill_trivials()
                    
                if dd and d == dd: 
                    self.B[i,j] = -d
                    self.fill_trivials()
                
                if ll and l == ll: 
                    self.B[i,j] = -l
                    self.fill_trivials()
                
                if rr and r == rr: 
                    self.B[i,j] = -r
                    self.fill_trivials()
                    
                if u and d and u == d: 
                    self.B[i,j] = -u
                    self.fill_trivials()
                    
                if l and r and l == r: 
                    self.B[i,j] = -l
                    self.fill_trivials()
             
        # Fill rows and columns. 
        for k in range(self.N): 
            if not np.all(self.B[k]) and (np.count_nonzero(self.B[k] == +1) == self.N // 2): 
                self.B[k, self.B[k] != +1] = -1
                self.fill_trivials()
                
            if not np.all(self.B[k]) and (np.count_nonzero(self.B[k] == -1) == self.N // 2): 
                self.B[k, self.B[k] != -1] = +1
                self.fill_trivials()
            
            if not np.all(self.B[:,k]) and (np.count_nonzero(self.B[:,k] == +1) == self.N // 2): 
                self.B[self.B[:,k] != +1, k] = -1
                self.fill_trivials()
                
            if not np.all(self.B[:,k]) and (np.count_nonzero(self.B[:,k] == -1) == self.N // 2): 
                self.B[self.B[:,k] != -1, k] = +1
                self.fill_trivials()
    
    def solve_rec(self, depth):
        ''' Recursion function for solving the puzzle with backtracking.'''
        
        if not self.check_progress(): return False # impossible branch. 
        if self.check_answer(): return True # solution found. 
        if not depth: return # recursion max depth reached. 
        
        for i in range(self.N):
            for j in range(self.N):
                
                if self.B[i,j]: continue
                
                branch_sun = deepcopy(self)
                branch_sun.B[i,j] = +1
                branch_sun.fill_trivials()
                rec_sun = branch_sun.solve_rec(depth-1)
                
                if rec_sun == False: 
                    self.B[i,j] = -1
                    continue
                elif rec_sun == True: 
                    self.B = branch_sun.B
                    return True
                
                branch_moon = deepcopy(self)
                branch_moon.B[i,j] = -1
                branch_moon.fill_trivials()
                rec_moon = branch_moon.solve_rec(depth-1)
                
                if rec_moon == False: 
                    self.B[i,j] = +1
                    continue
                elif rec_moon == True: 
                    self.B = branch_moon.B
                    return True
        
    def solve(self, B, marks): 
        ''' Solve the Tango puzzle given by an NxN board and its markings.'''
        
        self.B = B.copy()
        self.marks = marks
        
        self.fill_trivials()
        if self.solve_rec(depth=self.depth):
            return self.B      