'''
Created on 08/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Tuesday, December 01 2009
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
        '''
        TODO: Change this method. set_force should have an argument that is a 
        force. Not the elements to build that force 
        (also change names of arguments)
        '''

        model=self.model
        entity_id=self.entity_id
        
        try:
            model.detach_force(entity_id, self.last_force)
            
        except AttributeError:
            pass
        rel_position = self.get_relative_position()
        
        # store the current id of the force for future references
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
        '''
            TODO: THe if is for functionality. Is not efficient to do it this
            way. The best would be that the default value of 
            target_id=self.entity_id, but that is not working.
            Solution is to define that all this getters always need an argument
        '''
        if not target_id:
            rel_vel=self.model.get_relative_velocity(self.entity_id,
                                                     self.target_entity_id)
        else:
            rel_vel=self.model.get_relative_velocity(self.entity_id,target_id)
            
        return rel_vel
     
    def get_force(self):
        '''
        This method is used for combining behaviors. When a behavior is composed
        with other behaviors, instead of using the function update, we use the
        get_force function. 
        '''
        return self.model.forces[self.last_force]
    
    def get_heading(self,entity_id=None):
        '''
         Returns the normalized vector representing the heading of the unit
         WARNING: At the moment is the velocity
        '''
        return self.model.get_velocity(entity_id)        
        
     ########
     # Getters for grupal based steering
     
    def get_neighbors_id(self):
        #TODO: Get neighbors id in range, done by the model
        pass
     
    def get_neighbors_centriod(self,weights=None):
        #TODO: Get the centriod of the neighbors
        pass
        
    def get_neighbors_heading(self,weights=None):
        #TODO: Get the average heading of the neighbors
        pass

