'''
Created on Tuesday, November 24 2009

@author JuanPi Carbajal, Eze Pozzo
Last edit: Tuesday, November 24 2009
'''

def rotv(v,ang):
    # Based on the Octave implementation of Etienne Grossmann
    '''
     Generates the rotation matrix of angle around the vector v
    '''

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
