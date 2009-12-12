'''
Created on Sunday, November 08 2009

@author JuanPi Carbajal, Eze Pozzo
Last edit: Wednesday, November 18 2009
'''
from __future__ import division
import numpy as np
from numpy import array, diag, eye, concatenate, dot, pi, sqrt, ones, sin, transpose, kron, cos, zeros, vstack
from numpy.linalg import inv
from LinAlgebra_extra import rotv


class Transformation:
    '''
      A class that stores and applies the transformation
    '''   
    def __init__(self):
        '''
        Constructor
        '''
        self.T=self.T_inv=eye(3)
        
    def transform(self,Rcoord):
        
        v=concatenate((Rcoord,[1.0]))  
        return np.round(np.dot(self.T,np.transpose(v)))[:2]
       
    def inverse_transform(self, Scoord):
        '''
        returns approximate inverse of transform. transform(inverse_transform(X))!=X, 
        because transform is a projection
        '''
        v=concatenate((Scoord,[1.0]))
        return np.dot(self.T_inv, np.transpose(v))[:2]
     
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
       
        
        self.T_inv=inv(self.T)
        

