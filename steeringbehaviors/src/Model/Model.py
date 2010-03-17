'''
Created on 16/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Monday, December 07 2009
'''
from __future__ import division
import numpy as np
from numpy import add, dot, array, concatenate, sqrt, sin, cos

from Tools.LinAlgebra_extra import rotv, vector2angle

np.seterr(all='raise')
MAXSPEED=100.0
MAXANGSPEED=6.0
MAXFORCE=1000.0 # 60 N/kg, universal law! :D
MAXTORQUE=60.0 # 60 m * N/kg
DAMPING=0.0

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

        ##################
        # Force Realted attributes
        self.forces = []
        self.relative_forces = []
        self.total_force = copy.deepcopy(zero_vector)
        self.total_relative_force = copy.deepcopy(zero_vector)
        self.max_force = MAXFORCE

        ##################
        # Misc   
        self.id = None
        self.zero_vector = zero_vector
        self.mass = None
        self.inertia_moment = None
        
        ##################
        # Torque Realted attributes
        self.torques = []
        self.total_torque = 0.0
        self.max_torque = MAXFORCE

        ##################
        # State related attributes
        self.position = copy.deepcopy(zero_vector)
        self.velocity = copy.deepcopy(zero_vector)
        self.ang = None
        self.angspeed = None
        
    ##################
    # Force related methods
    
    def apply_force(self, force):
        '''
        Adds a force to the entity, can be deleted by calling remove_force with
        return id as parameter
        TODO: Allow variable forces.
        '''
        self.forces.append(force)
        self.total_force=add(self.total_force, force)

        return len(self.forces)-1
    
    def apply_relative_force(self, force):
        '''
        Adds a force to the entity, the force will be always expressed in the
        entity's internal coordinates
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
        self.total_relative_force=reduce(add, self.relative_forces,0)

    ##################
    # Torque related methods
    
    def apply_torque(self, torque):
        '''
        Adds a torque to the entity, can be deleted by calling remove_torque with
        return id as parameter
        TODO: Allow variable torques.
        '''
        self.torques.append(torque)
        self.total_torque=add(self.total_torque, torque)

        return len(self.torques)-1
    
    def remove_torque(self, torque_id):
        '''
        Removes a torque previously applied.
        '''
        del self.torques[torque_id]
        self.total_torque=reduce(add, self.torques, 0.0)
        
    
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
        self._centroid=dict()
        self._heading=dict()
        self._direction=dict()
        self._neighbours=dict()
        self.sensors=dict()
        
    def on_update(self, event):
        self.update(event['dt'])

    ###################
    #Getters
            
    def get_max_speed(self, entity_id):
        return MAXSPEED

    def get_max_angspeed(self, entity_id):
        return MAXANGSPEED

    def get_max_force(self,entity_id):
        return self.entities[entity_id].max_force

    def get_max_torque(self,entity_id):
        return self.entities[entity_id].max_torque
        
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
    
    def get_ang(self, entity_id):
        return self.entities[entity_id].ang

    def get_angspeed(self, entity_id):
        return self.entities[entity_id].angspeed
    
    def get_mass(self, entity_id):
        return self.entities[entity_id].mass

    def get_moment(self, entity_id):
        return self.entities[entity_id].intertia_moment
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
        DEPRECATED (?)
        '''
        force=np.array((cos(relative_angle), sin(relative_angle)))*magnitude
        
        force_id=self.entities[entity_id].apply_relative_force(force)
        return force_id
    
    def apply_rel_vec_force(self, entity_id, force):
        '''
        Applies a force relative to the entity's frame of reference.
        x component in the direction of the velocity
        y component in the direction perpendicular to the velocity 
        '''
        force_id=self.entities[entity_id].apply_relative_force(force)
        return force_id
            
    def detach_force(self, entity_id, force_id):
        self.entities[entity_id].remove_force(force_id)

    def detach_relative_force(self, entity_id, force_id):
        self.entities[entity_id].remove_relative_force(force_id)
                
    def apply_torque(self, entity_id, torque):
        '''
        Applies a torque relative to an inertial frame. You
        can think about a frame fixed to the floor.        '''
        torque_id=self.entities[entity_id].apply_torque(torque)
                
        return torque_id
    
    # Forcing Setters
    def set_ang(self,entity_id,ang):
        self.entities[entity_id].ang=ang
        
    def set_vel(self,entity_id,vel):
        self.entities[entity_id].velocity=vel

    def set_pos(self,entity_id,pos):
        self.entities[entity_id].position=pos
        
    def set_angspeed(self,entity_id,angspeed):
        self.entities[entity_id].angspeed=angspeed

    def set_mass(self,entity_id,mass):
        self.entities[entity_id].mass=mass
        # TODO: to fix when shapes are defined
        R=0.1
        self.entities[entity_id].inertia_moment=mass*R
            
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
        
    def get_entity(self, entity_id):
        '''
        Returns the list of entities
        '''
        return self.entities[entity_id]

    def add_entity(self, position=array((0.0,0.0)), velocity=array((0.0,0.0)),
                         ang=0.0,angspeed=0.0,mass=1.0):
        entity = Model_Entity( array((0.0,0.0)) )
        self.entities.append(entity)

        # Set identitty
        entity.id=len(self.entities)-1
        
        # Set state
        entity.position = array(position)
        entity.velocity = array(velocity)
        entity.ang = ang
        entity.angspeed = angspeed

        # Set physics
        self.set_mass(entity.id,mass)

        return len(self.entities) -1

    def on_damage(self, event):
        #DEPRECATED?
        entity_id=event['Damaged entity']
        self.grab_entity(entity_id)

    ###################   
    #Update
             
    def update(self, dt):
        '''
        dt in seconds
        integrates equations of motion
        '''
        rel2global_f=np.array([0.0,0.0])
        grabbed=self.grabbed
        
        #Erases precalculated neighbour values

        self._centroid=dict()
        self._heading=dict()
        self._direction=dict()
        self._neighbours=dict()
        
        dt_sec=dt
        self.reference_clock+=dt
        dt_2=dt_sec/2
        
        def verletV_step(ent):
            '''
                Perform one step of the verlet velocity algorithm
                Not vectorized
            '''
            # Put the forces given in the entity frame into the global frame
            # TODO: Put this in a function. Soon the entties wont be points 
            #       anymore and more projections/rotations will be needed.
            # There are three frames of reference:
            #       Global: 
            #               X axis horizontal pointing right,
            #               Y axis vertical  pointing down
            #       LocalVel (or LocalCourse):
            #               X axis parallel to velocity,
            #               Y axis perpendicular to velocity
            #       LocalHeading:
            #               X axis parallel to the direction the unit is
            #                pointing,
            #               Y axis perpendicular to that (defines the left of 
            #               the entity)
            #       We could define a transfrom in the model too using what is
            #       in real2pix.py

            # WARNING: The follwoing computation assumes relatives forces are
            # ginven in LocalCourse frame            
            ang = vector2angle(ent.velocity)
            R = rotv(array((0,0,1)), ang)[0:2,0:2]
            rel2global_f = np.dot(R, ent.total_relative_force)                

            # Update the total force                    
            force = (ent.total_force + rel2global_f) - DAMPING*ent.velocity
            
            # Update total torque
            # TODO: A factor accounting for the effective radius of the entity 
            #       is missing in the dmaping factor
            torque = ent.total_torque - DAMPING*ent.angspeed
            
            # Update vel(t+1/2) and position pos(t+1)
            v_2 = ent.velocity + force*dt_2/ent.mass
            ent.position = ent.position + v_2*dt_sec
            
            w_2 = ent.angspeed + torque*dt_2/ent.inertia_moment

            ent.ang = ent.ang + w_2*dt_sec
                
            # Update forces
            #ang = ent.ang = vector2angle(v_2)
            ang = vector2angle(v_2)
            R = rotv(array((0,0,1)), ang)[0:2,0:2]
            rel2global_f = np.dot(R, ent.total_relative_force)
            force = (ent.total_force + rel2global_f) - DAMPING*v_2
            
            # Update total torque
            # TODO: A factor accounting for the effective radius of the entity 
            #       is missing in the dmaping factor
            torque = ent.total_torque - DAMPING*w_2
                
            # Update vel(t+1)
            ent.velocity = v_2 + force*dt_2/ent.mass
            
            ent.angspeed = w_2 + torque*dt_2/ent.inertia_moment
            
            #ent.ang = vector2angle(v_2)        
            
        def ERM_step(ent):
            '''
                Euler-Richardson Method step
                "Numerical integration of Newton's equations including velocity
                dependent forces". 
                Ian R. Gatland. Am. J. Phys., Vol. 62, No. 3, March 1994
            '''
            # There are three frames of reference:
            #       Global: 
            #               X axis horizontal pointing right,
            #               Y axis vertical  pointing down
            #       LocalVel (or LocalCourse):
            #               X axis parallel to velocity,
            #               Y axis perpendicular to velocity
            #       LocalHeading:
            #               X axis parallel to the direction the unit is
            #                pointing,
            #               Y axis perpendicular to that (defines the left of 
            #               the entity)
            #       We could define a transfrom in the model too using what is
            #       in real2pix.py
            
            # WARNING: The follwoing computation assumes relatives forces are
            # ginven in LocalCourse frame            
            ang = vector2angle(ent.velocity)
            R = rotv(array((0,0,1)), ang)[0:2,0:2]
            rel2global_f = np.dot(R, ent.total_relative_force)                

            # Update the total force                    
            force = (ent.total_force + rel2global_f) - DAMPING*ent.velocity
            
            # Update total torque
            # TODO: A factor accounting for the effective radius of the entity 
            #       is missing in the damping factor
            torque = ent.total_torque - DAMPING*ent.angspeed
            
            # Update vel(t+1/2) and position pos(t+1/2)
            v_2 = ent.velocity + force*dt_2/ent.mass
            
            
            w_2 = ent.angspeed + torque*dt_2/ent.inertia_moment
            
            # Commented out. Used when forces depend on position and angle explicitly. Not programmed yet.
            # p_2 = ent.position + v_2*dt_2
            # a_2 = ent.ang + w_2*dt_2
                
            # Update forces
#            ang = ent.ang = vector2angle(v_2)
            ang = vector2angle(v_2)
            R = rotv(array((0,0,1)), ang)[0:2,0:2]
            rel2global_f = np.dot(R, ent.total_relative_force)
            force = (ent.total_force + rel2global_f) - DAMPING*v_2
            
            # Update total torque
            # TODO: A factor accounting for the effective radius of the entity 
            #       is missing in the damping factor
            torque = ent.total_torque - DAMPING*w_2
                
            # Update vel(t+1)
            ent.velocity = ent.velocity + force*dt_sec/ent.mass
            ent.angspeed = ent.angspeed + torque*dt_sec/ent.inertia_moment
            
            ent.position = ent.position + v_2*dt_sec
            ent.ang = ent.ang + w_2*dt_sec
                  
        for ent in self.entities:
            #TODO: Store the state of all the entities in a matrix and update
            #      all of them in a single operation.
            
            if ent.id in grabbed:
                continue
           
            #verletV_step(ent) 
            ERM_step(ent)
        
    def get_neighbour_average_heading(self, ent_id):
        try:
            heading=self._heading[ent_id]
        except KeyError:
            self.precalculate(ent_id)
            heading=self._heading[ent_id]
            
        return heading
    
    def get_neighbour_average_direction(self, ent_id):
        try:
            direction =self._direction[ent_id]
        except KeyError:
            self.precalculate(ent_id)
            direction =self._direction[ent_id]
        
        return direction
    
    def get_neighbour_centroid(self, ent_id):
        try:
            centroid =self._centroid[ent_id]
        except KeyError:
            self.precalculate(ent_id)
            centroid =self._centroid[ent_id]
        
        return centroid
    
    def get_neighbours(self, ent_id):
        try:
            nb =self._neighbours[ent_id]
        except KeyError:
            self.precalculate(ent_id)
            nb =self._neighbours[ent_id]
        
        return nb
    
    def set_neighbour_sensor(self, ent_id, radius, aperture):
        '''
        Defines a sensor for neighbor entities.
        '''
        self.sensors[ent_id]=radius, aperture
        
    def precalculate(self, ent_id):
        '''
        Calculates averages for all entities in sensor range of the given entity.
        DO NOT CALL DIRECTLY
        '''
        radius, aperture=self.sensors[ent_id]
        
        position=self.entities[ent_id].position
        in_range=set()   
        to_average=list()   
        angle=self.entities[ent_id].ang
        lower_angle=-aperture
        higher_angle=aperture
        sin_ang=sin(angle)
        cos_ang=cos(angle)

        for ent in self.entities:
            if ent.id==ent_id:
                continue
            rel_position=ent.position-position
            dx=rel_position[0]
            dy=rel_position[1]
                
            #Skip if entity is outside a box that contains the circle of radius radius
            if dx>radius or dx<-radius or dy>radius or dy<-radius:
                continue
                
            #Skip if outside the circle of radius radius                
            distance2=dx*dx+dy*dy
            if distance2>radius*radius:
                continue
            
            # Rotate the relative position vector to have 0 angle at entity direction          
            rot_rel_pos=array((rel_position[0]*cos_ang+rel_position[1]*sin_ang, \
                              -rel_position[0]*sin_ang +rel_position[1]*cos_ang ))
                
            # If unit is in sensor area add to do avergae
            rot_rel_ang=vector2angle(rot_rel_pos)
            if lower_angle<=rot_rel_ang<=higher_angle:
                    
                to_average.append(concatenate(\
              (ent.position, array((cos(ent.ang), sin(ent.ang))),ent.velocity)))
              
                in_range.add(ent.id)
        
        # Perform the averaging    
        try:
            average=reduce(add, to_average,0)*1.0/len(to_average)
        except ZeroDivisionError:
            average=array([0.0, 0.0, cos_ang, sin_ang, cos_ang, sin_ang])
     
        self._centroid[ent_id]=average[0:2]
        heading=average[2:4]
        heading=heading/sqrt(dot(heading, heading))
        self._heading[ent_id]=heading
        direction=average[4:6]
        try:
            direction=direction/sqrt(dot(direction, direction))
        except FloatingPointError:
            pass
        self._direction[ent_id]=direction
        self._neighbours[ent_id]=in_range


