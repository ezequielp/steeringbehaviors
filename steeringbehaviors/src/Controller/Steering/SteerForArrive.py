'''
Created on Saturday, November 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Wednesday, December 02 2009
'''

from numpy import sqrt, dot
from SteerForSeek import SteerForSeek

class SteerForArrive(SteerForSeek):
    '''
      Stops on arrival
      WARNING: THis function maynot work after the change of set_force on
      Wednesday, December 02 2009.
      TODO: Verify
    '''
    def __init__(self,model, entity_id):
        SteerForSeek.__init__(self, model, entity_id)
        self.slowing_distance=500
        
    def update(self, event=None):
        rel_position=self.get_relative_position(self.target_entity_id)
           
        distance=sqrt(dot(rel_position, rel_position))
        slowing_distance=self.slowing_distance
        if distance>slowing_distance:
            SteerForSeek.update(self, event)
        else:
            self.set_force(rel_position, 
                           self.max_speed*distance/slowing_distance)

