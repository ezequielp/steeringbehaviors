'''
Created on 08/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Saturday, November 28 2009
'''
from numpy import sqrt, dot
'''TODO: Dehack this. Probably must create/find an abstract vector class with v.norm() to avoid using directly'''
from Controller.Controller import Controller

class SteerController(Controller):
    '''
        Class containing all that a SteerFor** class will ever need :D
    '''
    
    def __init__(self, model, entity_id):
        self.model=model
        self.entity_id=entity_id
        self.max_speed=model.get_max_speed(entity_id)
    

    def update(self, event=None):
        '''
        Usual entry point on event handled environments
        '''
        # Here the controller updates the state of the entity
        self.update(event['dt'])

    # Methos for defining targets
    
    def target_entity(self, target_entity_id):
        # Targets another entitiy
        self.targeting_entity=True
        self.target_entity_id=target_entity_id
        
    def target_position(self, target_position):
        '''
        Not teleologically correct :D
        '''
        '''
        Targets a position in the model
        TODO: It should be merged with target_entity by defining a beacon entity 
        '''
        self.targeting_entity=False
        self.target_entity_id=None
        self.target_position=target_position
        
    ###################

    # Setter methods        
    
    def set_force(self, rel_position, max_speed):
        model=self.model
        entity_id=self.entity_id
        
        # Normalize the relative postion vector
        rel_position=rel_position*1.0/sqrt(dot(rel_position, rel_position))
        try:
            model.detach_force(entity_id, self.last_force)
            
        except AttributeError:
            pass
        
        # store the current value for future references
        self.last_force = model.apply_force(entity_id, rel_position*max_speed -\
                        model.get_velocity(entity_id))

    ###################

    # Getter methods        
    
    def get_relative_position(self):
        entity_id = self.entity_id
        
        if self.targeting_entity:
            rel_position = self.model.get_relative_position(entity_id, 
                           self.target_entity_id)
        else:
            rel_position = self.target_position - \
                           self.model.get_position(entity_id)
                           
                                                      
        return rel_position
        
    def get_abs_velocity(self,entity_id=None):
        return self.model.get_velocity(entity_id)
        
    def get_rel_velocity(self,target_id=None):
        if not target_id:
            rel_vel=self.model.get_relative_velocity(self.entity_id,
                                                     self.target_entity_id)
        else:
            rel_vel=self.model.get_relative_velocity(self.entity_id,target_id)
            
        return rel_vel
