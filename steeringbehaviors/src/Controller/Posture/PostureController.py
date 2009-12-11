'''
Created on Friday, December 11 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Friday, December 11 2009
'''
from numpy import sqrt, dot, array, cos , sin, pi
from Controller.Controller import Controller

class PostureController(Controller):
    '''
        Class containing all that a posture controller class will ever need :D
    '''
    
    def __init__(self, model, entity_id):
        self.model=model
        self.entity_id=entity_id
        self.max_angspeed=model.get_max_angspeed(entity_id)
        self.max_torque=model.get_max_torque(entity_id)    

    def update(self, event=None):
        '''
        Usual entry point on event handled environments
        '''
        # Here the controller updates the state of the entity
        self.update(event['dt'])

    # Methods for defining targets
    
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
    def set_torque(self, torque):
        '''
        This function receives the torque value to be applied
        '''
        model=self.model
        entity_id=self.entity_id
        
        try:
            model.detach_torque(entity_id, self.last_torque)
            
        except AttributeError:
            pass
        
        # store the current id of the force for future references
        self.last_torque = model.apply_torque(entity_id, torque)

    ###################

    # Getter methods        
    
    def get_relative_position(self,target_id):
        if self.targeting_entity:
            rel_position = self.model.get_relative_position(self.entity_id, 
                           target_id)
        else:
            rel_position = self.target_position - \
                           self.model.get_position(self.entity_id)
                           
                                                      
        return rel_position
        
    def get_rel_velocity(self,target_id):
        rel_vel=self.model.get_relative_velocity(self.entity_id,target_id)
          
        return rel_vel
     
    def get_torque(self):
        '''
        This method is used for combining controllers. When a controller is
        composed with other controllers, instead of using the function update, 
        we use the get_torque function. 
        '''
        return self.model.torques[self.last_torque]
    
    def get_heading_vec(self,entity_id):
        '''
         Returns the normalized vector representing the heading of the entity
        '''
        heading=self.model.get_ang(entity_id)
        return array((cos(heading),sin(heading)))

    def get_heading(self,entity_id):
        '''
         Returns the angle representing the heading of the entity
        '''
        return self.model.get_ang(entity_id)

    def get_course_vec(self,entity_id):
        '''
         Returns the normalized vector representing the course of the entity, 
         i.e. the normalized velocity
        '''
        course=self.get_abs_velocity(entity_id)
        try:
            course=course/sqrt(dot(course,course))
        except FloatingPointError:
            # If course is zero leave it zero
            pass
            
        return course
     
     ########
     # Getters for group based steering
     
    def get_neighbors_id(self):
        neighbors = self.model.get_neighbours(self.entity_id)
        return neighbors
        
    def get_neighbors_heading(self,weights=None):
        heading = self.model.get_neighbour_average_heading(self.entity_id)
        return heading

    def get_neighbors_course(self,weights=None):
        course = self.model.get_neighbour_average_direction(self.entity_id)
        return course

    ########
    # Limit checkers
    def check_torque(self,torque):
        if torque > self.max_torque:
            return self.max_torque
        return torque
    
