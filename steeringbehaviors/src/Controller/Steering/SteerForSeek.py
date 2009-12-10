'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Thursday, December 10 2009
'''
'''TODO: Ohashi, Yoshikazu (1994) "Fast Linear Approximations of Euclidean Distance 
         in Higher Dimensions", in Graphics Gems IV, Paul Heckbert editor, Academic
         Press. 
'''

from numpy import sqrt, dot
from SteerController import SteerController

class SteerForSeek(SteerController):
    '''
        Steers the unit towards the current position of the target
    '''
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force)
    
    def get_force(self):
        # Gets the vector pointing to the target
        rel_position=self.get_relative_position(self.target_entity_id)
        
        force=rel_position*self.max_force

        # Check for limit       
        fnorm=sqrt(dot(force,force))       
        if fnorm > self.max_force:
            force = force*self.max_force/fnorm
        
        return force

