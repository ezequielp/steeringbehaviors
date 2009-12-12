'''
Created on Monday, November 30 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Saturday, December 12 2009
'''

from numpy import sqrt, dot
from SteerController import SteerController

class SteerForOffset(SteerController):
    '''
     The entity approaches the target keeping a minimum distance
     Attribute offset is the distance
     Attribute side defines either left (1) or right(-1) respect to the 
     direction of motion of the target
    '''
    
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        self.offset=75
        self.side=1.0
        
    def update(self, event=None):
        force=self.get_force(event)
        self.set_force(force)

    #########
    # Getters
                    
    def get_force(self, event=None):
        target_id=self.target_entity_id
        entity_id=self.entity_id
        
        rel_position=self.get_relative_position(target_id)
        
        target_velocity=self.get_rel_velocity(target_id)
        
        '''
         Estimates the position fo the target in the next time step and 
         applies an offset
        '''
        future_target_pos=rel_position+target_velocity*event['dt']
        '''
         Get the perpendicular direction respect to the direction of the entity
         Then apply the offset to the future position fo target
        '''
        target_direction=self.get_rel_course_vec(target_id)

        offset = future_target_pos - \
                        dot(future_target_pos,target_direction)*target_direction
        
        # Scale to self.offset
        offset = self.side*self.offset*offset/sqrt(dot(offset,offset))     

        direction = future_target_pos+offset
        force = direction*self.max_force
        
        return self.check_force(force)

    def get_offset(self):
        return self.offset

    def get_side(self):
        return self.side
    
    #########
    # Setters
    def set_offset(self,value):
        self.offset=value

    def set_side(self,value):
        self.side=value
    
    #########
    # Tuners
    def increment_offset(self,increment):
        self.offset+=increment

    def scale_offset(self,factor):
        self.offset*=factor
        
