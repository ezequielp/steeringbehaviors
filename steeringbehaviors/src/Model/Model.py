'''
Created on 16/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Thursday, November 26 2009
'''
from __future__ import division
import numpy as np
from numpy import add, dot, array
from math import sin,cos,pi
from Tools.LinAlgebra_extra import rotv, vector2angle

np.seterr(all='raise')
verlet_v_integrator=False
Heun_f_integrator=True

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
    def __init__(self, zero_vector):
        '''
        TODO: Emit event when the model is created.
        '''
        import copy

        self.forces=[]
        self.relative_forces=[]
        self.total_force=copy.deepcopy(zero_vector)
        self.total_relative_force=copy.deepcopy(zero_vector)
        
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
        self.total_force=reduce(add, self.forces)

    def remove_relative_force(self, relative_force_id):
        del self.relative_forces[relative_force_id]
        self.total_relative_force=reduce(add, self.relative_forces)
    
    
class PhysicsModel(Model):
    def __init__(self):
        self.entities = []#WeakKeyDictionary()
        self.grabbed=set()
          
    def add_entity(self, position, velocity):
        entity=Model_Entity(array((0.0,0.0)))
        self.entities.append(entity)
        entity.position=array(position)
        entity.velocity=array(velocity)
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
        force=np.array((cos(relative_angle), sin(relative_angle)))*magnitude
        
        force_id=self.entities[entity_id].apply_relative_force(force)
        return force_id
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
           
            
            if ent.id in grabbed:
                continue
            
            ang=ent.ang=vector2angle(ent.velocity)

            # JPi: I thought the model was 3D, i.e. all forces arrays had 3 
            # elements. I guess that is the best way of doing it.
            # As a workaround I prefer to slice the rotation matrix rather than,
            # concatenate and then slice.
            
           # rel2global_f=np.dot(rotv(array((0,0,1)), ang), np.concatenate((ent.total_relative_force, [1])))[0:2]
            R=rotv(array((0,0,1)), ang)[0:2,0:2]
            rel2global_f=np.dot(R, ent.total_relative_force)                
                    
            force=(ent.total_force + rel2global_f)
            print np.dot(force, ent.velocity)
            
            if verlet_v_integrator:
                # Update vel(t+1/2) and position pos(t+1)
                dt_2=dt*1.0/2000
                v_2=ent.velocity+force*dt_2
                ent.position=ent.position+v_2*dt*(1.0/1000)
                '''
                Forces should be updated at this point, not needed for constant forces.
                '''
                # Update accelerations a(t+1) and vel(t+1)
                # JPI: Do we have to update the entities somehow?
                # Eze: Yes, Forces depend on velocity. Which means we can't use Verlet Velocity :(
                # TODO
                #Maybe  http://adsabs.harvard.edu/abs/1994AmJPh..62..259G
                # The usal election is Adam-Dashforth which is like a 
                # Runge-Kutta http://mymathlib.webtrellis.net/diffeq/adams_top.html
                # I will read the paper...I have nother one with lots of methds
                # I will check that one too. Anyway, I have a multigent simualtion
                # using the verlet and it works ok. It is not simplectic anymore
                # but is order 4.
                
                ang=ent.ang=vector2angle(v_2)
                R=rotv(array((0,0,1)), ang)[0:2,0:2]
                rel2global_f=np.dot(R, ent.total_relative_force)
                force=(ent.total_force + rel2global_f)
                #To calculate the new f(v) force... less error but still
                #Didn't find any simplectic algorithm to solve H(x,v) yet...
                
                ent.velocity=v_2+force*dt_2
                
            elif Heun_f_integrator:
                '''
            The so-call "Improved Euler" method, also known as the trapezoidal or bilinear or predictor/corrector or Heun Formula method, is a second order integrator.

                ppos=
 STATE predictor(state);
 predictor.x += state.v * dt;
 predictor.v += system.GetAcceleration(state) * dt;
 
 STATE corrector(state);
 corrector.x += predictor.v * dt;
 corrector.v += system.GetAcceleration(predictor) * dt;
 
 state.x = (predictor.x + corrector.x)*0.5;
 state.v = (predictor.v + corrector.v)*0.5;
'''
                # I don't think is the algorithm above, but lets see.
                # I think the algorithm is keeping track of the predictor and
                # the corrector, while I am just doing it for one time step.
                ppos=ent.position+ent.velocity*dt*(1.0/1e3)
                pvel=ent.velocity+force*dt*(1.0/1e3)
                cpos=ent.position+pvel*dt*(1.0/1e3)
                
                ang=vector2angle(pvel)
                R=rotv(array((0,0,1)), ang)[0:2,0:2]
                rel2global_f=np.dot(R, ent.total_relative_force)
                force=(ent.total_force + rel2global_f)
                
                cvel=ent.velocity+force*dt*(1.0/1e3)

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
                    ent.old_position=ent.position-ent.velocity*dt*1.0/1000
                    
               
                new_position=ent.position+ent.velocity*dt*1.0/1000+force*dt*dt*1.0/2000000
            
                ent.velocity=(new_position-ent.old_position)*500.0/dt
                
                ent.old_position=ent.position
                ent.position=new_position


        
