'''
Created on Monday, November 30 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Wednesday, December 02 2009
'''

from numpy import sqrt, dot
from SteerController import SteerController

class SteerForOffset(SteerController):
    '''
     The entity tries to keep a constant distance form the target
     Verified: Wednesday, December 02 2009 - Is working
     TODO: Impruve the repulsion when target is approaching 
    '''
    
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        self.offset_distance=75

    def update(self, event=None):
        # TODO: Parametrize this
        force=self.get_force(event)
        # Desired call
        #self.set_force(force)
        
        # Emulating damping
        self.set_force(300*force-self.get_abs_velocity(self.entity_id))
                
    def get_force(self, event=None):
        target_id=self.target_entity_id
        entity_id=self.entity_id
        
        rel_position=self.get_relative_position(target_id)
        
        target_velocity=self.get_rel_velocity(target_id)
        
        # Estimates the position fo the target in the next time step and 
        #applies an offset
        
        future_target_pos=rel_position+target_velocity*event['dt']
        '''
         Get the perpendicular direction respect to the direction of the entity
         Then apply the offset to the future position fo target
        '''
        entity_direction=self.get_heading_vec(entity_id)
#        entity_direction=self.get_abs_velocity(entity_id)
#        norm_dir=sqrt(dot(entity_direction,entity_direction))
#        if norm_dir > 0.0:
#            entity_direction=entity_direction/norm_dir

        offset=future_target_pos - \
                       dot(future_target_pos,entity_direction)*entity_direction
        offset=(-1)*self.offset_distance*offset/sqrt(dot(offset,offset))     

        direction = future_target_pos+offset
        #Normalize
        try:
            direction=direction*1.0/sqrt(dot(direction, direction))
        except FloatingPointError:
            pass
        
        return direction

