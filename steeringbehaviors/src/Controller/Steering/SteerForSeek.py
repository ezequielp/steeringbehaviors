'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Saturday, November 28 2009
'''
from numpy import sqrt, dot
from Controller.Controller import Controller
import SteerController

class SteerForSeek(SteerController):
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        
    def update(self, event=None):
        entity_id=self.entity_id
        
        rel_position=self.get_relative_position()
        '''TODO: Ohashi, Yoshikazu (1994) "Fast Linear Approximations of Euclidean Distance 
        in Higher Dimensions", in Graphics Gems IV, Paul Heckbert editor, Academic Press. 
        See ftp://princeton.edu/pub/Graphics/GraphicsGems/GemsIV/ <- Deadlink '''

        self.apply_force(rel_position, self.max_speed)

    def apply_force(self, rel_position, max_speed):
        model=self.model
        entity_id=self.entity_id

        rel_position=rel_position*1.0/sqrt(dot(rel_position, rel_position))
        
        try:
            model.detach_force(entity_id, self.last_force)
            
        except AttributeError:
            pass
        
        self.last_force=model.apply_force(entity_id, rel_position*max_speed-model.get_velocity(entity_id))
        
    def get_relative_position(self):
        entity_id=self.entity_id
        if self.targeting_entity:
            rel_position=self.model.get_relative_position(entity_id, self.target_entity_id)
        else:
            rel_position=self.model.get_position(entity_id)-self.target_entity_id
        return rel_position


