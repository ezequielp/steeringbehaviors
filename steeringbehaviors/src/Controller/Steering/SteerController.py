'''
Created on 08/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Wednesday, December 02 2009
'''
from numpy import sqrt, dot, array, cos , sin, pi
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
        
    def set_target_position(self, target_position):
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
    def set_force(self, rel_position, max_speed=0.0):
        '''
        TODO: Change this method. set_force should have an argument that is a 
        force. Not the elements to build that force 
        (also change names of arguments)
        '''
        '''
        This function receives the force vector to be applied
        '''
        model=self.model
        entity_id=self.entity_id
        
        # Normalize the relative position vector
        # JPi: Idem as below, this is not needed
        '''
        try:
            rel_position=rel_position*1.0/sqrt(dot(rel_position, rel_position))
        except FloatingPointError:
            pass
        '''    
        try:
            model.detach_force(entity_id, self.last_force)
            
        except AttributeError:
            pass
        
        # store the current id of the force for future references
        self.last_force = model.apply_force(entity_id, rel_position)

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
        
    def get_abs_velocity(self,entity_id):
        return self.model.get_velocity(entity_id)
        
    def get_rel_velocity(self,target_id):
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
    
    def get_heading_vec(self,entity_id):
        '''
         Returns the normalized vector representing the heading of the entity
        '''
        heading=self.model.get_ang(entity_id)
        return array((cos(heading),sin(heading)))

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
        
    def get_neighbors_centroid(self,weights=None):
        centroid = self.model.get_neighbour_centroid(self.entity_id)
        return centroid
        
    def get_neighbors_heading(self,weights=None):
        heading = self.model.get_neighbour_average_heading(self.entity_id)
        return heading

    def get_neighbors_course(self,weights=None):
        course = self.model.get_neighbour_average_direction(self.entity_id)
#        print self.entity_id,course
        return course

