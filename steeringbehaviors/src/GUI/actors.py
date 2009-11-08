'''
Created on 08/11/2009

@author: Guille
'''

from  GUI.config import *
import pygame
from pygame.sprite import Sprite
simple_sprite=pygame.Surface((6,6))
simple_sprite.fill((255,255,255))
simple_sprite.set_colorkey((255,255,255), pygame.RLEACCEL)


class BasicActor(Sprite):
    '''
    An autonomous entity that moves according to registered steering behaviors 
    '''

    def __init__(self, initial_position):
        '''
        Constructor
        '''
        Sprite.__init__(self)
        self._targets=dict()
        self._behaviors=dict()
        self.position=array(initial_position)
        self.rect=pygame.Rect(initial_position, (0,0))
        self.image=simple_sprite
        
        pygame.draw.circle(self.image, (0,0,0), (3,3), 3)
        
    def setTarget(self, target, behaviorClass):
        '''
        @target: An actor that has a position variable properly updated
        @behavior: A steering behavior class that has an "array get_steering_force(self, target)" method
        '''
        if not behaviorClass in self._targets.keys():
            self._targets[behaviorClass]=[target]
        else:
            self._targets[behaviorClass].append(target)
            
        if not behaviorClass in self._behaviors:
            self._behaviors[behaviorClass]=behaviorClass(self)
        
    def update(self, dt):
        totalForce=array(zero_tuple)
        for behaviorClass, allTargets in self._targets.iteritems():
            #print map(self._behaviors[behaviorClass].get_steering_force, allTargets)
            totalForce+=sum(map(self._behaviors[behaviorClass].get_steering_force, allTargets))
       
        self.position=self.position+totalForce*dt
        self.rect.center=self.position
        


class MouseActor(Sprite):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Sprite.__init__(self)
        self.position=array(zero_tuple)
        self.rect=pygame.Rect((0,0), (0,0))
        self.image=simple_sprite
        
    
    def update(self, dt):
        pass