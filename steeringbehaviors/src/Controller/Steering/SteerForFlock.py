'''
Created on Tuesday, December 01 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Tuesday, December 01 2009
'''

from numpy import sqrt, dot, array
from SteerController import SteerController

class SteerForFlock(SteerController):
    '''
    A controller that flocks.
    '''
    from SteerForCohesion import SteerForCohesion
    from SteerForSeparation import SteerForSeparation
    from SteerForAling import SteerForAling
    
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        aling=self.SteerForAling(model, entity_id)
        self.aling=aling.get_force
        group=self.SteerForCohesion(model, entity_id)
        self.group=group.get_force
        avoid=self.SteerForSeparation(model, entity_id)
        self.avoid=avoid.get_force
                
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force, self.max_speed)
        
    def get_force(self):
        
        force=self.aling()+self.group()+self.avoid()

        return force
               
