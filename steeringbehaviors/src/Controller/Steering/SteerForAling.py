'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Tuesday, December 01 2009
'''

from numpy import sqrt, dot
from SteerController import SteerController

class SteerForAling(SteerController):
    '''
    Alings the unit to the average aligment.
    WARNING: using velocity as the direction vector
    '''
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
                
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force, self.max_speed)
        
    def get_force(self):
        
        heading=self.get_neighbors_heading()

        force=heading-self.get_heading_vec(self.entity_id)
        
        try:
            force= force/sqrt(dot(force,force))
        except FloatingPointError:
            pass
       
        #Return the force
        return force
               
