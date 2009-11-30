'''
Created on Monday, November 30 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Monday, November 30 2009
'''

from numpy import sqrt, dot
from SteerController import SteerController

class SteerForOffset(SteerController):

    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        self.offset_distance=50
        
    def update(self, event=None):
        model=self.model
        target_id=self.target_entity_id
        entity_id=self.entity_id
        
        rel_position=self.get_relative_position()
        
        target_velocity=self.get_rel_velocity(target_id)
        
        entity_direction=self.get_abs_velocity(entity_id)
        norm_dir=sqrt(dot(entity_direction,entity_direction))
        if norm_dir > 0.0:
            entity_direction=entity_direction/norm_dir

        # Stimates the position fo the target in the next time step and applies an offset
        future_target_pos=rel_position+target_velocity*event['dt']
        '''
         Get the perpendicular direction respect to the direction of the entity
         WARNING: Using velocity as direction
         Then apply the offset to the future position fo target
        '''
        offset=future_target_pos - \
                         dot(future_target_pos,entity_direction)*entity_direction
        offset=(-1)*self.offset_distance*offset/sqrt(dot(offset,offset))     

        self.set_force(future_target_pos+offset,self.max_speed)

