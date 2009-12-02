'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Wednesday, December 02 2009
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
        WARNING: After Wednesday, December 02 2009 may not work as desired
        TODO: Verify
    '''
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force)
    
    def get_force(self):
        # Gets the vector pointing to the target
        rel_position=self.get_relative_position(self.target_entity_id)
        
        #Normalize
        try:
            rel_position=rel_position*1.0/sqrt(dot(rel_position, rel_position))
        except FloatingPointError:
            pass
            
        # JPi: correction due to e-mail of Wednesday, December 02 2009
        force=rel_position*self.max_speed -self.get_abs_velocity(self.entity_id)
        
        return force

