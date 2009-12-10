'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Thursday, December 10 2009
'''

from numpy import sqrt, dot, array
from SteerController import SteerController

class SteerForCohesion(SteerController):
    '''
    Steers the entity towards the centriod of its neighbors.
    '''

    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
                
    
    
    def update(self, event=None):
        force=self.get_force()
        
        self.set_force(force)
        
    def get_force(self):
        
        center=self.get_neighbors_centroid()
        
        self.set_target_position(center)
        
        # Gets the vector pointing to the target
        rel_position=self.get_relative_position(self.target_entity)
    
        # Apply force in that direction
        force=rel_position*self.max_force

        # Check for limit       
        fnorm=sqrt(dot(force,force))       
        if fnorm > self.max_force:
            force = force*self.max_force/fnorm

        #Return the force
        return force


