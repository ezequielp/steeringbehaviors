'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Saturday, December 12 2009
'''
from numpy import sqrt, dot
from SteerController import SteerController

class SteerForFlee(SteerController):
    '''
       Is just the opposite of SteerForSeek
    '''
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
            
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force)
    
    def get_force(self):
        # Gets the vector pointing to the entity from the target
        rel_position=(-1)*self.get_relative_position(self.target_entity_id)
        
        norm2=dot(rel_position,rel_position)
        force=(rel_position/norm2)*self.max_force

        return self.check_force(force)
