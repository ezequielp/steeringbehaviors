'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Saturday, November 28 2009
'''

from numpy import sqrt, dot
from SteerForSeek import SteerForSeek

class SteerForArrive(SteerForSeek):
    def __init__(self,model, entity_id):
        SteerForSeek.__init__(self, model, entity_id)
        self.slowing_distance=500
        
    def update(self, event=None):
        rel_position=self.get_relative_position()
           
        distance=sqrt(dot(rel_position, rel_position))
        slowing_distance=self.slowing_distance
        if distance>slowing_distance:
            SteerForSeek.update(self, event)
        else:
            self.apply_force(rel_position, self.max_speed*distance/slowing_distance)

