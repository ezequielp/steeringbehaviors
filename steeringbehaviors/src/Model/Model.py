'''
Created on 16/11/2009

@author: Ezequiel N. Pozzo
'''
from weakref import WeakKeyDictionary
import numpy as np

class Model(object):
    '''
    Abstract model. 
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        assert False, "Abstract object"
        
    def update(self, dt):
        '''
        Updates state
        '''
        assert False, "Must implement"


class Model_Entity(object):
    '''
    An abstract entity on the model.
    '''
    position=None
    def __init__(self):
        '''
        TODO: Emit event when the model is created.
        '''
        self.forces=[]
        
    def apply_force(self, force):
        '''
        Adds a force to the entity, can be deleted by calling remove_force with return id as parameter
        '''
        self.forces.append(force)
        self.total_force=np.add(self.total_force, force)

        return len(self.forces)-1
        
    def remove_force(self, force_id):
        del self.forces[force_id]
        self.total_force=reduce(np.add, self.forces)

        
    def calculate_total_force
    
class PhysicsModel(Model):
    def __init__(self):
        self.entities = []#WeakKeyDictionary()
          
    def add_entity(self, position, velocity):
        entity=Model_Entity()
        self.entities.append(entity)
        entity.position=np.array(position)
        entity.velocity=np.array(velocity)
        
        return len(self.entities) -1
        
    def delete_entity(self, entity_id):
        del self.entities[entity_id]
        
    def apply_force(self, entity_id, force):
        force_id=self.entities[entity_id].apply_force(np.array(force))
                
        return force_id
        
    def detach_force(self, entity_id, force_id):
        self.entities[entity_id].remove_force(force_id)
        
        
    def update(self, dt):
        '''
        Using:
        1. actualize velocidad con aceleracion actual dt/2 -> v(t+1/2)=v(t)+a(t)*dt/2
        2. actualize posicion x(t+1)=x(t)+v(t+1/2)*dt
        3. actualize acclereacion a(t+1)=f(x(t+1))/m
        4. actualize velocidad v(t+1)=v(t+1/2)+a(t+1)*dt/2
        '''
        for entity in self.entities:
            entity.position=

        