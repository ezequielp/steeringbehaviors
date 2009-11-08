'''
Created on Sunday, November 08 2009

@author JuanPi Carbajal
'''
from __future__ import division
from numpy import * #reduce at the end

def _set_transfrom(move=array([0,0])), rotate=array([0]),scale=array([1,1])):
    # Works only in 2D for the moment                                 
                    
    # Create transfromation
    A = matrix(eye(2))
    
    # Rotation
    R =eye([3,3])
    # needs rotv
    
    # Scale
    S = diag(concatenate([scale,[1]]))
       
    # Translation
    T = zeros([3,3])
    for i in xrange(0,2)
        T[i,-1]=move[i]

    # total
    A=R*S+T
    
def rotv(v,ang=0.0):

#if ang != 0.0
#  v = v.*((ang(:)./sqrt(sum(v'.^2))')*ones(1,3));
#end

#a = sqrt(sum(v'.^2))' ; 
#oka = find(a!=0);
#if all(size(oka)),
#  v(oka,:) = v(oka,:)./(a(oka)*ones(1,3)) ; 
#end

#N = size(v,1) ; N3 = 3*N ;
#r = (reshape( v', N3,1 )*ones(1,3)).*kron(v,ones(3,1)) ;
#r += kron(cos(a),ones(3,3)) .* (kron(ones(N,1),eye(3))-r) ;

#tmp = zeros(N3,3) ;
#tmp( 2:3:N3,1 ) =  v(:,3) ;
#tmp( 1:3:N3,2 ) = -v(:,3) ;
#tmp( 3:3:N3,1 ) = -v(:,2) ;
#tmp( 1:3:N3,3 ) =  v(:,2) ;
#tmp( 2:3:N3,3 ) = -v(:,1) ;
#tmp( 3:3:N3,2 ) =  v(:,1) ;

#r -= kron(sin(a),ones(3)) .* tmp ;


