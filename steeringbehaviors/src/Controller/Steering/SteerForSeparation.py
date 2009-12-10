'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Thursday, December 10 2009
'''
from __future__ import division
from numpy import sqrt, dot, array
from SteerController import SteerController

class SteerForSeparation(SteerController):
    '''
    Steers the unit away from its neighbors using a repulsion force
    proportional to 1/r (in th eimplentation is divided by 1/r^2 but one is
    to normalize the direction)
    '''

    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
                
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force, self.max_speed)
        
    def get_force(self):
        
        others_id=self.get_neighbors_id()
        
        #TODO: Is this somewhere?
        force=array([0.0,0.0])
        
        for neighbor in others_id:
            self.target_entity(neighbor)
            
            # Gets the vector pointing to the entity from the target
            rel_position=(-1)*self.get_relative_position(self.target_entity_id)
            
            # Square norm

            norm2=dot(rel_position, rel_position)

            try:     
                force += rel_position/norm2
            except FloatingPointError:
                pass
        
        # Check for limit       
        fnorm=sqrt(dot(force,force))       
        if fnorm > self.max_force:
            force = force*self.max_force/fnorm

        #Return the force
        return force
               
