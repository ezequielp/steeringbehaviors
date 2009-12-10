'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Thursday, December 10 2009
'''

from numpy import sqrt, dot
from SteerForSeek import SteerForSeek

class SteerForArrive(SteerForSeek):
    '''
      Stops on arrival
    '''
    def __init__(self,model, entity_id):
        SteerForSeek.__init__(self, model, entity_id)
        self.slowing_distance=500

    def update(self, event=None):
        force=self.get_force(event)
        self.set_force(force)        
        
    def get_force(self, event=None):
        rel_position=self.get_relative_position(self.target_entity_id)
           
        distance=sqrt(dot(rel_position, rel_position))
        slowing_distance=self.slowing_distance
        
        if distance>slowing_distance:
            force=SteerForSeek.get_force(self, event)
        else:
            force=rel_position*self.max_force/slowing_distance

        return force

