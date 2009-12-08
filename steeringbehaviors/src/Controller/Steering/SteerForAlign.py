'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Tuesday, December 08 2009
'''

from numpy import sqrt, dot,array
from SteerController import SteerController

class SteerForAlign(SteerController):
    '''
    Alings the unit to the average aligment.
    WARNING: The force is normalized
    Verified: Tuesday, December 08 2009 - Is working
    '''
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
                
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force)
        
    def get_force(self):
        # Get the normalized average velocity of the neighbours       
        course=self.get_neighbors_course()
        
        # Apply a force that turns the entity in that direction
        force=course-self.get_course_vec(self.entity_id)
        
        # Normalize
        try:
            force= force/sqrt(dot(force,force))
        except FloatingPointError:
            pass
        
        #Return the force
        return force
               
