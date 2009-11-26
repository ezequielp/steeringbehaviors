'''
Created on 08/11/2009

@author: Ezequiel N. Pozzo
'''
from numpy import sqrt, dot
from Controller import Controller

class steerForSeek(Controller):
    def __init__(self, model, entity_id):
        self._model=model
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
        
    def update(self, event):
        model=self._model
        entity_id=self.entity_id
        
        if self.targeting_entity:
            rel_position=model.get_relative_position(entity_id, self.target_entity_id)
        else:
            rel_position=model.get_position(entity_id)-self.target_entity_id
            
        '''TODO: Ohashi, Yoshikazu (1994) “Fast Linear Approximations of Euclidean Distance 
        in Higher Dimensions”, in Graphics Gems IV, Paul Heckbert editor, Academic Press. 
        See ftp://princeton.edu/pub/Graphics/GraphicsGems/GemsIV/ '''
        from numpy import dot
        rel_position=rel_position*1.0/dot(rel_position, rel_position)
        
        model.apply_force(entity_id, rel_position*self.max_speed-model.get_velocity(entity_id))
            
        
        
    def on_update(self, event):
        self.update(event['dt'])