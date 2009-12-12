'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Saturday, December 12 2009
'''

from numpy import sqrt, dot,array
from SteerController import SteerController

class SteerForAlign(SteerController):
    '''
    Aligns the unit to the average velocity direction.
    '''
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
                
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force)

    ########
    # Getters
             
    def get_force(self):
        # Get the normalized average velocity of the neighbours       
        course=self.get_neighbors_course()
        
        # Apply a force that turns the entity in that direction
        force=course-self.get_course_vec(self.entity_id)

        #Return the force
        return self.check_force(force)
    
    
               
