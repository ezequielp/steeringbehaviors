'''
Created on Sunday, November 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Saturday, December 12 2009
'''
from numpy import sqrt, dot
from SteerController import SteerController

class SteerForFlee(SteerController):
    '''
       Is just the opposite of SteerForSeek.
       The attribute safe_distance is the value of the distance to the taget
       such that F=force_max/10
    '''
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        self.safe_distance=1.0
            
    def update(self, event=None):
        force=self.get_force()
        self.set_force(force)
    
    #######
    # Getters

    def get_force(self,event=None):
        # Gets the vector pointing to the entity from the target
        rel_position=self.get_relative_position(self.target_entity_id)
        
        norm2 = dot(rel_position,rel_position)
        force =(-0.1)*(rel_position/norm2)*self.safe_distance*self.max_force

        return self.check_force(force)

    def get_safe_distance(self):
        return self.safe_distance
        
    #######
    # Setters
    def set_safe_distance(self,distance):
        self.safe_distance=distance
        
