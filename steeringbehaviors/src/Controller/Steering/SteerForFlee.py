'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Sunday, November 29 2009
'''
from numpy import sqrt, dot
from SteerController import SteerController

class SteerForFlee(SteerController):
    '''
       Is just the opposite of SteerForSeek
    '''
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
            
    def update(self, event=None):
        entity_id=self.entity_id

        # Gets the vector pointing away from the target
        rel_position=(-1)*self.get_relative_position()

        # Applies a force in the sense of that vector
        self.set_force(rel_position, self.max_speed)
