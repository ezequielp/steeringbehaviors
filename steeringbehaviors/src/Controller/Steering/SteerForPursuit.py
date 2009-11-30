'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Sunday, November 29 2009
'''

from numpy import sqrt, dot
from SteerController import SteerController

class SteerForPursuit(SteerController):

    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)

    def update(self, event=None):
        model=self.model
        target_id=self.target_entity_id
        entity_id=self.entity_id
        
        rel_position=self.get_relative_position()
        
        target_velocity=self.get_rel_velocity(target_id)
        
        # Stimates the position of the target in the next time step and
        # Applies a force in that direction
        self.set_force(rel_position+target_velocity*event['dt'],
                         self.max_speed)

