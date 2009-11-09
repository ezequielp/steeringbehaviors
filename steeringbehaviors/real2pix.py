'''
Created on Sunday, November 08 2009

@author JuanPi Carbajal
'''
from __future__ import division
from numpy import * #reduce at the end
import numpy as np

class transformation:
    '''
      A class that stores and applies the transformation
    '''   
    def __init__(self):
        '''
        Constructor
        '''
        self.T=eye(3)
        self.A=array([0,0])
        
    def transform(self,Rcoord):
        #Why all the 2D to 3D and back?
        v=concatenate((Rcoord,[1.0]))  
        
        return np.round(np.dot(self.T,np.transpose(v))[:2]+self.A)
        
    def _set_transform(self,move=array([0,0]), rotate=array([0]),scale=array([1,1])):
        # Works only in 2D for the moment                                 
                    
        # Rotation
        R = rotv(array([0,0,1]),rotate[0])
        # Scale
        S = diag(concatenate([scale,[1]]))
        
        # Translation
        self.A = move
        '''zeros([3,3])
        for i in xrange(0,2):
            A[i,-1]=move[i]*scale[i]'''
        

        # total->This wasn't right... Rotation+Translation is not homogeneous: vt=RS*v+A
        self.T=dot(R,S)#+A
        
    
def rotv(v,ang):
    # Based on the Octave implementation of Etienne Grossmann

      a = ang*pi/180.0
      v = v/sqrt(dot(v,v))
      r = transpose( vstack((v,v,v)) ) * kron(v,ones([3,1])) 
      r = r + cos(a)*ones([3,3]) * (eye(3)-r) 

      tmp = zeros([3,3]) 
      tmp[1,0] =  v[2] 
      tmp[0,1] = -v[2] 
      tmp[2,0] = -v[1]
      tmp[0,2] =  v[1]
      tmp[1,2] = -v[0]
      tmp[2,1] =  v[0]
  
      r = r + sin(a)*ones([3,3]) * tmp ;

      return r
