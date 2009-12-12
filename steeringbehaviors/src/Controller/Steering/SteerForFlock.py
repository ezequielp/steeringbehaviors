'''
Created on Tuesday, December 01 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Thursday, December 10 2009
'''

from numpy import sqrt, dot, array
from SteerController import SteerController

class SteerForFlock(SteerController):
    '''
    A controller that flocks.
    TODO: How to distribute the intensities?
    '''
    from SteerForCohesion import SteerForCohesion
    from SteerForSeparation import SteerForSeparation
    from SteerForAlign import SteerForAlign
    
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        self.align=self.SteerForAlign(model, entity_id)
        self.group=self.SteerForCohesion(model, entity_id)
        self.avoid=self.SteerForSeparation(model, entity_id)
               
    def update(self, event=None):
        force=self.get_force([1,500,500])
        
        self.set_force(1*force-0.0*self.get_abs_velocity(self.entity_id))
        
    def get_force(self,weights=[0,0,0]):
        
        force= weights[0]*self.group.get_force() + \
               weights[1]*self.avoid.get_force()+ \
               weights[2]*self.align.get_force()

        # Check for limit       
        fnorm=sqrt(dot(force,force))       
        if fnorm > self.max_force:
            force = force*self.max_force/fnorm

        return force
               
