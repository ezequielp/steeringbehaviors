'''
Created on 08/11/2009

@author: Ezequiel N. Pozzo
'''
from numpy import sqrt, dot
'''TODO: Dehack this. Probably must create/find an abstract vector class with v.norm() to avoid using directly'''
from Controller.Controller import Controller

class SteerController(Controller):
    def __init__(self, model, entity_id):
        self.model=model
        self.entity_id=entity_id
        self.max_speed=model.get_max_speed(entity_id)
    
    def target_entity(self, target_entity_id):
        self.targeting_entity=True
        self.target_entity_id=target_entity_id
        
    def target_position(self, target_position):
        '''
        Not teleologically correct :D
        '''
        self.targeting_entity=False
        self.target_entity_id=None
        self.target_position=target_position
        
    def update(self, event=None):
        '''
        Usual entry point on event handled environments
        '''
        self.update(event['dt'])
        
        
class SteerForSeek(SteerController):
    def __init__(self, model, entity_id):
        SteerController.__init__(self, model, entity_id)
        
    def update(self, event=None):
        entity_id=self.entity_id
        
        rel_position=self.get_relative_position()
        '''TODO: Ohashi, Yoshikazu (1994) "Fast Linear Approximations of Euclidean Distance 
        in Higher Dimensions", in Graphics Gems IV, Paul Heckbert editor, Academic Press. 
        See ftp://princeton.edu/pub/Graphics/GraphicsGems/GemsIV/ '''

        self.apply_force(rel_position, self.max_speed)

    def apply_force(self, rel_position, max_speed):
        model=self.model
        entity_id=self.entity_id

        rel_position=rel_position*1.0/sqrt(dot(rel_position, rel_position))
        
        try:
            model.detach_force(entity_id, self.last_force)
            
        except AttributeError:
            pass
        
        self.last_force=model.apply_force(entity_id, rel_position*max_speed-model.get_velocity(entity_id))
        
    def get_relative_position(self):
        entity_id=self.entity_id
        if self.targeting_entity:
            rel_position=self.model.get_relative_position(entity_id, self.target_entity_id)
        else:
            rel_position=self.model.get_position(entity_id)-self.target_entity_id
        return rel_position
           
   
        
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

            
class SteerForPursuit(SteerForSeek):
    def __init__(self, model, entity_id):
        SteerForSeek.__init__(self, model, entity_id)

    def update(self, event=None):
        model=self.model
        target_id=self.target_entity_id
        entity_id=self.entity_id
        
        rel_position=self.get_relative_position()
        
        target_velocity=model.get_velocity(target_id)
        
        self.apply_force(rel_position-target_velocity*event['dt']*1.0/1000, self.max_speed)
        
        