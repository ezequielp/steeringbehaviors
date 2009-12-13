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
        self.set_relative_force(force)
        #self.set_force(force)        

    ########
    # Getters
        
    def get_force(self, event=None):
        # The force generated is in the frame of reference that has
        # the velocity as X axis
        
        # Vector form target to seeker and normalization and perpendicular
        r =  (-1)*self.get_relative_position(self.target_entity_id)
        r_hat=r
        try:
            r_hat = r / sqrt(dot(r,r))
        except FloatingPointError:
            # If zero leave it zero
            pass
        perp2rhat=array((-r_hat[1],r_hat[0]))
        
        # Relative velocity, perpendicular to it and normalization
        v = self.get_rel_velocity(self.target_entity_id)
       
        # control action and force
        # Basically: Keep the relative velocity parallel to the 
        # relaitve position
        action = self.gain*(dot(-perp2rhat,v))
        rel_force = array((0.0, action))

        return self.check_force(rel_force)
    
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
