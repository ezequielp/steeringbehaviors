'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Wednesday, December 02 2009
'''

from numpy import sqrt, dot,array
from SteerController import SteerController

class SteerForAlign(SteerController):
    '''
    Alings the unit to the average aligment.
    WARNING: The force is normalized
    Verified: Wednesday, December 02 2009 - Is working
    '''
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
                
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force)
        
    def get_force(self):
        
        heading=self.get_neighbors_heading()
        
        force=heading-self.get_heading_vec(self.entity_id)
        
        try:
            force= force/sqrt(dot(force,force))
        except FloatingPointError:
            return array((0.0,0.0))
        
        
        #Return the force
        return force
               
