'''
Created on 16/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Tuesday, November 24 2009
'''
from weakref import WeakKeyDictionary
import numpy as np
from Tools.LinAlgebra_extra import rotv, vector2angle

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
        assert False, "Not implemented"

    def grab_entity(self, entity_id):
        '''
        Makes the entity fixed and unable to react to the environment
        '''
        assert False, "Not implemented"
        
    def drop_entity(self, entity_id):
        '''
        Returns the entity to its normal behavior
        '''
        assert False, "Note implemented"

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
        self.grabbed=set()
          
    def add_entity(self, position, velocity):
        entity=Model_Entity()
        self.entities.append(entity)
        entity.position=np.array(position)
        entity.velocity=np.array(velocity)
        entity.id=len(self.entities)-1
        return len(self.entities) -1
        
    def delete_entity(self, entity_id):
        del self.entities[entity_id]
        
    def grab_entity(self, entity_id):
        self.grabbed.add(entity_id)
        
    def drop_entity(self, entity_id):
        self.grabbed.remove(entity_id)
        
    def move_entity(self, entity_id, position):
        self.get_entity(entity_id).position=position
        
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
        
        
    def on_update(self, event):
        self.update(event['dt'])
        
    def update(self, dt):
        '''
        dt in miliseconds
        Using:
        1. actualize velocidad con aceleracion actual dt/2 -> v(t+1/2)=v(t)+a(t)*dt/2
        2. actualize posicion x(t+1)=x(t)+v(t+1/2)*dt
        3. actualize acclereacion a(t+1)=f(x(t+1))/m
        4. actualize velocidad v(t+1)=v(t+1/2)+a(t+1)*dt/2
        '''
        rel2global_f=np.array([0,0])
        grabbed=self.grabbed
        for ID , ent in enumerate(self.entities):
            '''
            Thinking out loud: This is not efficient, I think we could use matrices to store all velocities
            positions and forces, and do this without any loop. Requires model redesign but should have mayor
            performance improvement.
            '''
            # Rotate the forces in the frame of the entity to the global frame
            # The direction of Y axis of the entity is asusmed coincident with 
            # the direction of the velocity.
            # TODO: generalize this
            
            ang=vector2angle(ent.velocity)          #TODO: vector2angle
            rel2global_f=np.dot(rotv(ang,[0,0,-1]),relative_force[ID])
            
            # Update vel(t+1/2) and position pos(t+1)
            if ent in grabbed:
                continue
            v_2=ent.velocity+(ent.total_force+rel2global_f)*(dt*1.0/1000)/2)
            ent.position=ent.position+v_2*dt*(1.0/1000)
            
            '''
            Forces should be updated at this point, not needed for constant forces.
            '''
            # Update accelerations a(t+1) and vel(t+1)
            # JPI: Do we have to update the entities somehow?
            # TODO
            
            ent.velocity=v_2+(ent.total_force+rel2global_f)*dt/2*(1.0/1000)
            


        
