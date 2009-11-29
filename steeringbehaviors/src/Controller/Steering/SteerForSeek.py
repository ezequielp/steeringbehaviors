'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Sunday, November 29 2009
'''
'''TODO: Ohashi, Yoshikazu (1994) "Fast Linear Approximations of Euclidean Distance 
         in Higher Dimensions", in Graphics Gems IV, Paul Heckbert editor, Academic
         Press. 
'''

from numpy import sqrt, dot
from SteerController import SteerController

class SteerForSeek(SteerController):

    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        
    def update(self, event=None):
        entity_id=self.entity_id
        
        # Gets the vector pointing to the target
        rel_position=self.get_relative_position()

        # Applies a force in the sense of that vector
        self.set_force(rel_position, self.max_speed)



