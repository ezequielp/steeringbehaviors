'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Wednesday, December 02 2009
'''

from numpy import sqrt, dot, array
from SteerController import SteerController

class SteerForCohesion(SteerController):
    '''
    Steers the entity towards the centriod of its neighbors.
    WARNING: At the moment the force is normalized
    Verified: Wednesday, December 02 2009 - Is working
    '''

    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
                
    
    
    def update(self, event=None):
        force=self.get_force()
        
        self.set_force(force)
        
    def get_force(self):
        
        center=self.get_neighbors_centriod()

        self.set_target_position(center)
       
        # Gets the vector pointing to the target
        rel_position=self.get_relative_position()
        # Normalize
        try:
            rel_position=rel_position/sqrt(dot(rel_position, rel_position))
        except FloatingPointError:
            
            pass
        #Return the force
        return rel_position


