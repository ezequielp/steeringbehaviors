'''
Created on Saturday, December 12 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Saturday, December 12 2009
'''

from numpy import sqrt, dot, array
from SteerController import SteerController

class SteerForMC(SteerController):
    '''
    Approachs the target usign Motion Camouflage
    Adaptation from E.W. Justh and P.S. Krishnaprasad, 
    'Steering laws for motion camouflage' http://arxiv.org/abs/math/0508023
    Adapted by Juan Pablo Carbajal
    ajuanpi@gmail.com
    
    Attributes:
        gain: How strong does the ocntroller acts. The bigger the better, but
        depends a lot on the maximum values of force and velocities, damping...
        etc
    '''
    
    def __init__(self,model, entity_id):
        SteerController.__init__(self, model, entity_id)
        self.gain = .5
        
    def update(self, event=None):
        force=self.get_force(event)
        self.set_force(force)        

    ########
    # Getters
        
    def get_force(self, event=None):
        
        # Vector form target to seeker and normalization
        r =  (-1)*self.get_relative_position(self.target_entity_id)
        r_hat=r
        try:
            r_hat = r / sqrt(dot(r,r))
        except FloatingPointError:
            # If zero leave it zero
            pass
        
        # Relative velocity, perpendicular to it and normalization
        v = self.get_rel_velocity(self.target_entity_id)
        perp2v = array((-v[1],v[0]))
        norm=sqrt(dot(v,v))

        n2v_hat=v
        v_hat=v
        try:
            n2v_hat = perp2v / norm
            v_hat = v / norm
        except FloatingPointError:
            # If zero leave it zero
            pass
            
        
        # control action and force
        action = -self.gain*(dot(r_hat,perp2v))
        force = (n2v_hat - v_hat)*action

        return self.check_force(force)
    
    def get_gain(self):
        return self.gain

    ########
    # Setters

    def set_gain(self,value):
        self.gain=value

    ########
    # Tuners
    def increment_gain(self,increment):
        self.gain+=increment

    def scale_gain(self,factor):
        self.gain*=factor
