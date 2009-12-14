'''
Created on Saturday, December 12 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal 
Last Edit: Saturday, December 12 2009
'''

from numpy import sqrt, dot
from SteerForSeek import SteerForSeek

class SteerForTrack(SteerForSeek):
    '''
      Tracks the target from certain distance using a damped spring
      Attributes:
        tracking_distance is the desired distance
        breaking_intensity, higher then it breaks faster smaller it oscillates
        correction_intensity, the level of reaction to the errors
    '''
    def __init__(self,model, entity_id):
        SteerForSeek.__init__(self, model, entity_id)
        self.tracking_distance = 70
        self.breaking_intensity = 1
        self.correction_intensity = 5 
        
    def update(self, event=None):
        force=self.get_force(event)
        self.set_force(force)        

    ########
    # Getters
        
    def get_force(self, event=None):
       
        rel_position=self.get_relative_position(self.target_entity_id)
        distance=sqrt(dot(rel_position, rel_position))
        delta_d=self.tracking_distance - distance
        
        vel=self.get_rel_velocity(self.target_entity_id)
        
        force = -self.correction_intensity*delta_d*rel_position/distance + \
                 self.breaking_intensity * vel
                                    
        return self.check_force(force)
    
    def get_rel_force(self, event=None):
        '''
        Gives the force in the LC (local course) frame. The X component is
        parallel to the velocity of the entity
        '''
        rel_position=self.get_relative_position(self.target_entity_id)
        distance=sqrt(dot(rel_position, rel_position))
        delta_d=self.tracking_distance - distance
        
        vel=self.get_rel_velocity(self.target_entity_id)
        vel=sqrt(dot(vel,vel))
        
        force = array((-self.correction_intensity * delta_d +\
        self.breaking_intensity * vel,0.0))

        return self.check_force(force)
    
    def get_tracking_distance(self):
        return self.tracking_distance

    def get_breaking_intensity(self):
        return self.breaking_intensity

    def get_correction_intensity(self):
        return self.correction_intensity
        
    ########
    # Setters

    def set_slowing_distance(self,distance):
        self.slowing_distance=distance

    def set_breaking_intensity(self,value):
        self.breaking_intensity=value

    def set_correction_intensity(self,value):
        self.correction_intensity=value
    
    ########
    # Tuners
    def increment_distance(self,increment):
        self.tracking_distance+=increment

    def increment_breaking(self,increment):
        self.breaking_intensity+=increment

    def increment_correction(self,increment):
        self.correction_intensity+=increment
    
    def scale_distance(self,factor):
        self.tracking_distance*=factor

    def scale_breaking(self,factor):
        self.breaking_intensity*=factor

    def scale_correction(self,factor):
        self.correction_intensity*=factor
        
