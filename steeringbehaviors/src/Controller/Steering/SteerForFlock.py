'''
Created on Tuesday, December 01 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Tuesday, December 01 2009
'''

from numpy import sqrt, dot, array
from SteerController import SteerController

class SteerForFlock(SteerController):
    '''
    Alings the unit to the average aligment.
    WARNING: using velocity as the direction vector
    '''
    from SteerForCohesion import SteerForCohesion
    from SteerForSeparation import SteerForSeparation
    from SteerForAling import SteerForAling
    
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        self.aling=SteerForAling.get_force
        self.group=SteerForCohesion.get_force
        self.avoid=SteerForSeparation.get_force
                
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force, self.max_speed)
        
    def get_force(self):
        
        force=self.aling()+self.group()+self.avoid()

        return force
               
