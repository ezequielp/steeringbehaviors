'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Saturday, November 28 2009
'''

from numpy import sqrt, dot
import SteerForSeek

class SteerForPursuit(SteerForSeek):
    def __init__(self, model, entity_id):
        SteerForSeek.__init__(self, model, entity_id)

    def update(self, event=None):
        model=self.model
        target_id=self.target_entity_id
        entity_id=self.entity_id
        
        rel_position=self.get_relative_position()
        
        target_velocity=model.get_velocity(target_id)
        
        self.apply_force(rel_position-target_velocity*event['dt']*1.0/1000, self.max_speed)

