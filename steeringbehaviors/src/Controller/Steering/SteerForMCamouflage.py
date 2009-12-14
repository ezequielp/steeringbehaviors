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
        force=self.get_rel_force(event)
        self.set_relative_force(force)

    ########
    # Getters
        
    def get_rel_force(self, event=None):
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
        
class SteerForMCHeading(SteerController):
    '''
    Approachs the target usign Motion Camouflage applied to the heading of the
    target. It is the equivalent to the previous one when the heding and the
    course are parallel.
    
    Attributes:
        gain: How strong does the ocntroller acts. The bigger the better, but
        depends a lot on the maximum values of force and velocities, damping...
        etc
    '''
    
    def __init__(self,model, entity_id):
        SteerController.__init__(self, model, entity_id)
        self.gain = .5
        
    def update(self, event=None):
        force=self.get_rel_force(event)
        self.set_relative_force(force)

    ########
    # Getters
        
    def get_rel_force(self, event=None):
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
        
        # Get relative heading 
        h = self.get_rel_heading_vec(self.target_entity_id) 
        try:
            h_hat = h / sqrt(dot(h,h))
        except FloatingPointError:
            # If zero leave it zero
            pass
        perp2h=array((-h_hat[1],h_hat[0]))
        
        v = self.get_rel_velocity(self.target_entity_id)
        velperp2h = dot(v,perp2h)* perp2h
        
#        print h,self.get_heading_vec(self.target_entity_id),self.get_rel_velocity(self.target_entity_id)
        # control action and force
        # Basically: Keep the relative velocity parallel to the 
        # relative position
        action = (-1)*self.gain*(dot(perp2rhat,velperp2h))
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
