'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Thursday, December 10 2009
'''
from numpy import sqrt, dot
from SteerController import SteerController

class SteerForFlee(SteerController):
    '''
       Is just the opposite of SteerForSeek
       Verified: Wednesday, December 02 2009 - Is working
       TODO: Here damping is in the force itself... 
    '''
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
            
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force)
    
    def get_force(self):
        # Gets the vector pointing to the entity from the target
        rel_position=(-1)*self.get_relative_position(self.target_entity_id)
        
        force=rel_position*self.max_force
        
        # Check for limit       
        fnorm=sqrt(dot(force,force))       
        if fnorm > self.max_force:
            force = force*self.max_force/fnorm

        return force
