'''
Created on Tuesday, December 01 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Wednesday, December 02 2009
'''

from numpy import sqrt, dot, array
from SteerController import SteerController

class SteerForFlock(SteerController):
    '''
    A controller that flocks.
    Verified: Wednesday, December 02 2009 - Is working
      TODO: How to distribute the intensities?
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
        
        self.set_force(10*force-self.get_abs_velocity(self.entity_id))
        
    def get_force(self):
        
        force= 100*self.aling.get_force() + 20*self.group.get_force() + \
              200*self.avoid.get_force() 
        
        return force
               
