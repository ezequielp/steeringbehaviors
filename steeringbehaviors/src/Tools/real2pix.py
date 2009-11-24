'''
Created on Sunday, November 08 2009

@author JuanPi Carbajal, Eze Pozzo
Last edit: Wednesday, November 18 2009
'''
from __future__ import division
import numpy as np
from numpy import array, diag, eye, concatenate, dot, pi, sqrt, ones, sin, transpose, kron, cos, zeros, vstack
from LinAlgebra_extra import rotv


class Transformation:
    '''
      A class that stores and applies the transformation
    '''   
    def __init__(self):
        '''
        Constructor
        '''
        self.T=eye(3)
        
    def transform(self,Rcoord):
        #Why all the 2D to 3D and back?
        # JPi: Is not 2D 3D is homogenous coordinates. You have to append a
        # one to the end (or beginning, depending on convention) so that 
        # translations are linear transformations (and not affine). If the 
        # vectors were 3D here we woudl have a 4D vector.
        # Ezeq: gotcha
        v=concatenate((Rcoord,[1.0]))  
        
        return np.round(np.dot(self.T,np.transpose(v)))[:2]
        
    def set_transform(self,move=array([0,0]), rotate=array([0]),scale=array([1,1])):
        # Works only in 2D for the moment                                 
                    
        # Rotation
        R = rotv(array([0,0,1]),rotate[0])
        # Scale
        S = diag(concatenate([scale,[1]]))
        
        # Translation
        A = zeros([3,3])
        for i in xrange(0,2):
            A[i,-1]=move[i]*scale[i]

        self.T=dot(R,S)+A
        
    

