'''
Created on Tuesday, November 24 2009

@author JuanPi Carbajal, Eze Pozzo
Last edit: Thursday, November 26 2009
'''
from math import pi, sqrt, cos, sin
from numpy import transpose, dot, vstack, kron, ones, zeros, eye, arctan2

def rotv(v,ang):
    # Based on the Octave implementation of Etienne Grossmann
    '''
     Generates the rotation matrix of angle around the vector v
     Angle is in radias
    '''

    a = ang
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
    
def vector2angle(v,w=None):
    '''
       Get the angle between the X axis and the direction defined by v.
       The angle is in (-pi, pi] range
       If w is given then it is taken as the reference
       TODO: Check efficiency of this implementation
    '''
    if w != None:
        ang2 = arctan2(v[1], v[0])
        ang1 = arctan2(w[1], w[0])
        dang = ang2 - ang1
        while dang > pi :
            dang = dang - 2.0*pi
        while dang < -pi :
            dang = dang + 2.0*pi
        
        return dang     
    else:  
        return arctan2(v[1], v[0])
    
