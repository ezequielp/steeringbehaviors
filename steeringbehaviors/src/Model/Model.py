'''
Created on 16/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Tuesday, December 01 2009
'''
from __future__ import division
import numpy as np
from numpy import add, dot, array
from math import sin,cos,pi
from Tools.LinAlgebra_extra import rotv, vector2angle

np.seterr(all='raise')
verlet_v_integrator=False
verlet_friction=False

Heun_f_integrator=True
MAXSPEED=300

class Model(object):
    '''
    Registers DAMAGE_EVENT:
        damaged entity: id
        damaging entity: id
        damage: integer
    '''
    
    def __init__(self, event_handler):
        '''
        Constructor
        '''
        self.event_handler=event_handler
        self.DAMAGE_EVENT=event_handler.new_event_type()
        event_handler.bind(self.on_damage,self.DAMAGE_EVENT)
        
        
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
    def __init__(self, zero_vector):
        '''
        TODO: Emit event when the model is created.
        '''
        import copy

        self.forces=[]
        self.relative_forces=[]
        self.total_force=copy.deepcopy(zero_vector)
        self.total_relative_force=copy.deepcopy(zero_vector)
        self.zero_vector=zero_vector
        self.ang=0
        
    
    def apply_force(self, force):
        '''
        Adds a force to the entity, can be deleted by calling remove_force with return id as parameter
        TODO: Allow variable forces.
        '''
        self.forces.append(force)
        self.total_force=add(self.total_force, force)

        return len(self.forces)-1
    
    def apply_relative_force(self, force):
        '''
        Adds a force to the entity, the force will be always expressed in the entity's internal coordinates
        Returns the id of the relative force
        '''
        self.relative_forces.append(force)
        self.total_relative_force=add(self.total_relative_force, force)
        
        return len(self.relative_forces)-1
        
        
    def remove_force(self, force_id):
        '''
        Removes a force previously applied.
        '''
        del self.forces[force_id]
        self.total_force=reduce(add, self.forces, self.zero_vector)

    def remove_relative_force(self, relative_force_id):
        del self.relative_forces[relative_force_id]
        self.total_relative_force=reduce(add, self.relative_forces)
    
class VelocityEstimator(object):
    '''
    Calculates a series of points based on the historic set of time,positions
    '''
    def __init__(self):
        from collections import deque
        self.positions=deque([],2)
    
    def append(self, time, new_position):
        '''
        Adds a new position to estimator model
        '''
        from copy import deepcopy
        self.positions.append((time, deepcopy(new_position)))
        
    def get_velocity_estimation(self):
        last_time, last_position=self.positions[-1]
        try:
            first_time, first_position=self.positions[-2]
        except IndexError:
            return last_position*0
        
        if last_time-first_time>0:
            return (last_position-first_position)*1.0/(last_time-first_time)
        else:
            return last_position*0
        
class PhysicsModel(Model):
    def __init__(self, event_handler):
        Model.__init__(self, event_handler)
        self.entities = []#WeakKeyDictionary()
        self.grabbed=set()
        self.reference_clock=0
        self.velocity_estimator=dict()
          
    def on_update(self, event):
        self.update(event['dt'])

    ###################
    #Getters
            
    def get_max_speed(self, entity_id):
        return MAXSPEED

    def get_position(self, entity_id):
        return self.get_entity(entity_id).position
    
    def get_relative_position(self, entity1_id, entity2_id):
        '''Returns the position of entitiy 2 respect to entity 1'''
        return self.get_entity(entity2_id).position-self.get_entity(entity1_id).position
    
    def get_velocity(self, entity_id):
        return self.get_entity(entity_id).velocity
        
    def get_relative_velocity(self, entity1_id,entity2_id):
        '''Returns the velocity of entitiy 2 respect to entity 1'''
        return self.get_entity(entity2_id).velocity-self.get_entity(entity1_id).velocity
    
    
    ###################
    # Entity related
    def delete_entity(self, entity_id):
        del self.entities[entity_id]
        
    def grab_entity(self, entity_id):
        self.grabbed.add(entity_id)
        
    def drop_entity(self, entity_id):
        self.grabbed.remove(entity_id)
        
    def move_entity(self, entity_id, position):
        '''
        Moves the entity to its new position. 
        It also updates the velocity to an average velocity using a simple estimator.
        '''
        estimator=self.velocity_estimator
        try:
            estimator[entity_id].append(self.reference_clock, position)
        except KeyError:
            estimator[entity_id]=VelocityEstimator()
            estimator[entity_id].append(self.reference_clock, position)
            
        entity=self.get_entity(entity_id)
        entity.position=position
        entity.velocity=estimator[entity_id].get_velocity_estimation()
        
    def get_entity(self, id):
        '''
        Returns the list of entities
        '''
        return self.entities[id]

    def add_entity(self, position, velocity):
        entity=Model_Entity(array((0.0,0.0)))
        self.entities.append(entity)
        entity.position=array(position)
        entity.velocity=array(velocity)
        entity.id=len(self.entities)-1
        return len(self.entities) -1

    def on_damage(self, event):
        id=event['Damaged entity']
        self.grab_entity(id)

    ###################    
    # Setters
    
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
        force=np.array((cos(relative_angle), sin(relative_angle)))*magnitude
        
        force_id=self.entities[entity_id].apply_relative_force(force)
        return force_id
        #self.total_relative_forces[entity_id]+=
        
    def detach_force(self, entity_id, force_id):
        self.entities[entity_id].remove_force(force_id)
        
 
    ###################   
    #Update
             
    def update(self, dt):
        '''
        dt in seconds
        Using:
        1. actualize velocidad con aceleracion actual dt/2 -> v(t+1/2)=v(t)+a(t)*dt/2
        2. actualize posicion x(t+1)=x(t)+v(t+1/2)*dt
        3. actualize acclereacion a(t+1)=f(x(t+1))/m
        4. actualize velocidad v(t+1)=v(t+1/2)+a(t+1)*dt/2
        '''
        rel2global_f=np.array([0,0])
        grabbed=self.grabbed
        
        # TODO: Where do we put this?
        dt_sec=dt
        self.reference_clock+=dt
        dt_2=dt_sec/2
        
        for ent in self.entities:
            #TODO: Store the state of all the entities in a matrix and update
            #      all of them in a single operation.
            
            if ent.id in grabbed:
                continue
            
            # Put the forces given in the entity frame into the global frame
            # TODO: Put this in a function. Soon the entties wont be points 
            #       anymore and more projections/rotations will be needed.
            ang=ent.ang=vector2angle(ent.velocity)
            R=rotv(array((0,0,1)), ang)[0:2,0:2]
            rel2global_f=np.dot(R, ent.total_relative_force)                

            # Update the total force                    
            force=(ent.total_force + rel2global_f)
            
            if verlet_v_integrator:
                # Update vel(t+1/2) and position pos(t+1)
                v_2=ent.velocity+force*dt_2
                ent.position=ent.position+v_2*dt_sec
               
                # Update forces
                ang=ent.ang=vector2angle(v_2)
                R=rotv(array((0,0,1)), ang)[0:2,0:2]
                rel2global_f=np.dot(R, ent.total_relative_force)
                force=(ent.total_force + rel2global_f)
               
                # Update vel(t+1)
                ent.velocity=v_2+force*dt_2
                
            elif Heun_f_integrator:
                '''
                The so-call "Improved Euler" method, also known as the trapezoidal 
                or bilinear or predictor/corrector or Heun Formula method, is a 
                second order integrator.
                '''
                # I don't think is the algorithm above, but lets see.
                # I think the algorithm is keeping track of the predictor and
                # the corrector, while I am just doing it for one time step.
                ppos=ent.position+ent.velocity*dt_sec
                pvel=ent.velocity+force*dt_sec
                cpos=ent.position+pvel*dt_sec
                
                ang=vector2angle(pvel)
                R=rotv(array((0,0,1)), ang)[0:2,0:2]
                rel2global_f=np.dot(R, ent.total_relative_force)
                force=(ent.total_force + rel2global_f)
                
                cvel=ent.velocity+force*dt_sec

                ent.position=(ppos + cpos)*0.5
                ent.velocity=(pvel + cvel)*0.5
                ent.ang=vector2angle(ent.velocity)
            else:
                '''
                verlet normal
                '''
                try:
                    ent.old_position
                except:
                    ent.old_position=ent.position-ent.velocity*dt_sec
                    
               
                new_position=ent.position+ent.velocity*dt_sec+0.5*force*dt_sec*dt_sec
            
                ent.velocity=(new_position-ent.old_position)*dt_2
                
                ent.old_position=ent.position
                ent.position=new_position
            
        
