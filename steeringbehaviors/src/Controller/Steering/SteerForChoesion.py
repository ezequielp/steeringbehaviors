'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Sunday, November 29 2009
'''

from numpy import sqrt, dot
from SteerController import SteerController

class SteerForCohesion(SteerController):

    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
                
    pass
    
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force, self.max_speed)
        
    def get_force(self):
        
        center=self.get_neighbors_centriod()
        
        target_position(center)
        
        # Gets the vector pointing to the target
        rel_position=self.get_relative_position()
        # Normalize
        rel_position=rel_position/sqrt(dot(rel_position, rel_position))
        
        #Return the force
        return rel_position


