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
        self.breaking_intensity=10
        
    def update(self, event=None):
        force=self.get_force(event)
        self.set_force(force)        

    ########
    # Getters
        
    def get_force(self, event=None):
        rel_position=self.get_relative_position(self.target_entity_id)
           
        distance=sqrt(dot(rel_position, rel_position))
        
        '''        
                if distance>slowing_distance:
                    force=SteerForSeek.get_force(self)
                else:
                    #force=rel_position/slowing_distance
                    force=
        '''
        force=SteerForSeek.get_force(self)
        if distance<self.slowing_distance:
            force = force - self.breaking_intensity * \
                                    self.get_rel_velocity(self.target_entity_id)

        return self.check_force(force)
    
    def get_slowing_distance(self):
        return self.slowing_distance

    def get_breaking_intensity(self):
        return self.breaking_intensity
        
    ########
    # Setters

    def set_slowing_distance(self,distance):
        self.slowing_distance=distance

    def set_breaking_intensity(self,distance):
        self.breaking_intensity=distance
    
    ########
    # Tuners
    def increment_slowing(self,increment):
        self.slowing_distance+=increment

    def increment_breaking(self,increment):
        self.breaking_intensity+=increment
    
    def scale_slowing(self,factor):
        self.slowing_distance*=factor

    def scale_breaking(self,factor):
        self.breaking_intensity*=factor
        
