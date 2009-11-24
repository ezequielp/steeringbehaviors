'''
Created on 16/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Tuesday, November 24 2009
'''
from weakref import WeakKeyDictionary
import numpy as np
from Tools.LinAlgebra_extra import rotv

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
        self.total_force=np.array((0.0, 0.0))
        
    def apply_force(self, force):
        '''
        Adds a force to the entity, can be deleted by calling remove_force with return id as parameter
        TODO: Allow variable forces.
        '''
        self.forces.append(force)
        self.total_force=np.add(self.total_force, force)

        return len(self.forces)-1
        
    def remove_force(self, force_id):
        '''
        Removes a force previously applied.
        '''
        del self.forces[force_id]
        self.total_force=reduce(np.add, self.forces)

    
    
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
        
    def get_entity(self, id):
        '''
        Returns the list of entities
        '''
        return self.entities[id]
    
    def apply_force(self, entity_id, force):
        '''
        Applies a force relative to an inertial frame. You
        can think about a frame fixed to the floor.
        You can also think of this as a more efficient way of doing the
        more teleologically correct "apply this force relative to my *current*
        system of reference"
        
        returns None
        '''
        force_id=self.entities[entity_id].apply_force(np.array(force))
                
        return force_id
        
    def apply_relative_force(self, entity_id, relative_angle, magnitude):
        '''
        Applies a force relative to the entity's frame of reference.
        The force will always be oriented relative_angle degrees from the 
        entity's orientation.
        The entity's orientation is the last non 0 velocity's direction.
        TODO: Make orientation independent of velocity?
        '''
        self.relative_forces[entity_id].add((relative_angle, magnitude))
        #self.total_relative_forces[entity_id]+=
        
    def detach_force(self, entity_id, force_id):
        self.entities[entity_id].remove_force(force_id)
        
        
    def update(self, dt):
        '''
        dt in miliseconds
        Using:
        1. actualize velocidad con aceleracion actual dt/2 -> v(t+1/2)=v(t)+a(t)*dt/2
        2. actualize posicion x(t+1)=x(t)+v(t+1/2)*dt
        3. actualize acclereacion a(t+1)=f(x(t+1))/m
        4. actualize velocidad v(t+1)=v(t+1/2)+a(t+1)*dt/2
        '''
        for ent in self.entities:
            '''
            Thinking out loud: This is not efficient, I think we could use matrices to store all velocities
            positions and forces, and do this without any loop. Requires model redesign but should have mayor
            performance improvement.
            '''
            v_2=ent.velocity+ent.total_force*(dt*1.0/1000)/2
            ent.position=ent.position+v_2*dt*(1.0/1000)
            '''
            Forces should be updated at this point, not needed for constant forces.
            '''
            ent.velocity=v_2+ent.total_force*dt/2*(1.0/1000)
            


        
