'''
Created on Friday, December 11 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal

Last Edit: Friday, December 11 2009
'''

#from numpy import sqrt, dot,array
from Tools.LinAlgebra_extra import vector2angle

from PostureController import PostureController

P=0.1

class LookAt(PostureController):
    '''
    Keeps a taget at 0 bearing with a proportional strategy
    '''
    def __init__(self, model, entity_id):
        PostureController.__init__(self, model, entity_id)
                
    def update(self, event=None):
        torque=self.get_torque()
        self.set_torque(torque)
        
    def get_torque(self):
        # Get angle to rotate
        ang_to_rot = vector2angle(self.get_rel_position(self.taget_entity_id)) -\
                                                self.get_heading(self.entity_id)
        # Estimate torque
        torque = - P * ang_to_rot

        #Return the torque
        return self.check_torque(torque)
               
