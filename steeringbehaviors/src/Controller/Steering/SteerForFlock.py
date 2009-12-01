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
        self.aling=self.SteerForAling(model, entity_id)
        self.group=self.SteerForCohesion(model, entity_id)
        self.avoid=self.SteerForSeparation(model, entity_id)
               
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force, self.max_speed)
        
    def get_force(self):
        
        force=self.aling.get_force() + self.group.get_force() + \
              self.avoid.get_force()

        return force
               
