'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Tuesday, December 01 2009
'''
from __future__ import division
from numpy import sqrt, dot, array
from SteerController import SteerController

class SteerForSeparation(SteerController):

    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
                
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force, self.max_speed)
        
    def get_force(self):
        
        others_id=self.get_neighbors_id()

        #TODO: Is this anywhere?
        force=array([0.0,0.0])

        for neighbor in others_id:
            self.target_entity(neighbor)
            
            # Gets the vector pointing to the target
            rel_position=(-1)*self.get_relative_position()
            
            # Sqaure norm

            norm2=dot(rel_position, rel_position)
            try:     
                force += rel_position/norm2
            except FloatingPointError:
                force += rel_position
        
        #Return the force
        return force
               
