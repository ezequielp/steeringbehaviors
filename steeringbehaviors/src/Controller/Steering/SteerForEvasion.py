'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Saturday, December 12 2009
'''

from numpy import sqrt, dot
from SteerController import SteerController

class SteerForEvasion(SteerController):
    '''
    Steers the entity away form the estimated next position of the target
    The attribute safe_distance is the value of the distance to the taget
    such that F=force_max/10
    '''

    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        self.safe_distance=1.0
        
    def update(self, event=None):
        force=self.get_force(event)
        self.set_force(force)

    #######
    # Getters
        
    def get_force(self, event=None):
        model=self.model
        target_id=self.target_entity_id
        entity_id=self.entity_id
        
        rel_position=self.get_relative_position(target_id)
        
        target_velocity=self.get_rel_velocity(target_id)
        
        # Estimates the position of the target in the next time step and
        # Applies a force repeling from that direction decreasing with distance
        future_target_pos=rel_position+target_velocity*event['dt']
        norm2=dot(future_target_pos,future_target_pos)
        
        force=(-0.1)*(future_target_pos/norm2)*self.safe_distance*self.max_force
        
        return self.check_force(force)

    def get_safe_distance(self):
        return self.safe_distance
        
    #######
    # Setters
    def set_safe_distance(self,distance):
        self.safe_distance=distance

