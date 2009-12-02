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
      Verified: Wednesday, December 02 2009 - Is working
      TODO: Improve the approahcing, could be an error there
    '''
    def __init__(self,model, entity_id):
        SteerForSeek.__init__(self, model, entity_id)
        self.slowing_distance=500

    def update(self, event=None):
        # TODO: Parametrize this
        force=self.get_force(event)
        # Desired call
        #self.set_force(force)
        
        # Emulating damping
        self.set_force(20*force-self.get_abs_velocity(self.entity_id))        
        
    def get_force(self, event=None):
        rel_position=self.get_relative_position(self.target_entity_id)
           
        distance=sqrt(dot(rel_position, rel_position))
        slowing_distance=self.slowing_distance
        if distance>slowing_distance:
            force=SteerForSeek.get_force(self, event)
        else:
            force=rel_position*self.max_speed/slowing_distance
            # was: set_force(rel_position,self.max_speed*distance/slowing_distance)
        return force

