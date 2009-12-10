'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Thursday, December 10 2009
'''

from numpy import sqrt, dot
from SteerController import SteerController

class SteerForEvasion(SteerController):
    '''
    Steers the entity away form the estimated next position of the target
    TODO: Improve the repulsion when target is approaching
    '''

    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
    
    def update(self, event=None):
        force=self.get_force(event)
        self.set_force(force)
        
    def get_force(self, event=None):
        model=self.model
        target_id=self.target_entity_id
        entity_id=self.entity_id
        
        rel_position=self.get_relative_position(target_id)
        
        target_velocity=self.get_rel_velocity(target_id)
        
        # Estimates the position of the target in the next time step and
        # Applies a force repeling from that direction
        future_target_pos=rel_position+target_velocity*event['dt']
        
        force=(-1)*future_target_pos*self.max_force
        
        # Check for limit       
        fnorm=sqrt(dot(force,force))       
        if fnorm > self.max_force:
            force = force*self.max_force/fnorm
            
        return 

