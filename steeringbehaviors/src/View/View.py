'''
Created on 16/11/2009

@author: Ezequiel N. Pozzo
Edited by JuanPi Carbajal
'''
from __future__ import division
import numpy as np
from Tools import real2pix as rp
import config

class View(object):
    '''
    An abstract class for Viewers
    '''
    def __init__(self, Model):
        self.model=Model
        
    def add_new_entity(self, model_entity):
        ''' 
        Ugly hack that will be solved when using events. Implement in concrete class
        TODO: implement as a event handler function add_new_entity(self, event)
        '''
        assert False, "Not implemented"
        
    def delete_entity(self, model_entity):
        '''
        Must be implemented in concrete class
        TODO: implement as event handler
        '''
        assert False, "Not implemented"

class View2D(View):
    '''
    A class for Viewers of 2D Models
    '''
    def __init__(self,Model):
        # Base class initialization 
        View.__init__(self, Model)
       
        # JPi: How do we define private variables and methods?
        # 18.11.09 : Prefix "_" means private
        self._sprites=np.array([])
        self._project=rp.Transformation()
    
    def update(self):
        # Here sprites are updated. How? Idea: apply the transformation
        # self._project.transformation(Model.actors) or something like that.
        # 
        pass
    
    def set_transform(self,move=np.array([0,0]), 
                           rotate=np.array([0]),
                           scale=np.array([1,1])):
        self._project.set_transform(move, rotate, scale)
        

class PygameViewer(View2D):
    '''
    A class rendering the actors of the Model into a Pygame window
    '''        
    import pygame
    from pygame.sprite import Sprite as SpriteParent

    class Sprite(SpriteParent):
        def __init__(self, model_entity):
            '''
            @model_entity_position: the position of the model object. Use [position] to get reference!!!
            '''
            pygame=PygameViewer.pygame
            PygameViewer.SpriteParent.__init__(self)
            self.model=model_entity
            
            self.rect=pygame.Rect(self.__project(model_entity.position), (0,0))
            
            '''
            TODO: implement better and more versatile method to set sprite image
            '''
            simple_sprite=pygame.Surface((6,6))
            simple_sprite.fill((255,255,255))
            simple_sprite.set_colorkey((255,255,255), pygame.RLEACCEL)
            self.image=simple_sprite
        
            pygame.draw.circle(self.image, (0,0,0), (3,3), 3.0)
            
            
        def update(self):
            self.rect.center=self.__project.transform(self.model.position)
        
        
    def __init__(self, Model):
        View2D.__init__(self, Model)
        pygame=self.pygame
        pygame.init()
        self.Sprite.__project=self.project
        self.sprites=self.pygame.sprite.RenderUpdates()
        
        
    
        from weakref import WeakKeyDictionary
        self.sprite_from_model=WeakKeyDictionary()
        
        '''
        Starts a simple black screen.
        TODO: improve to be configurable
        '''
        self.screen=pygame.display.set_mode(config.screen_size)
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))
        self.background=background
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        
    def update(self):
        self.sprites.clear(self.screen, self.background)
        self.sprites.update()
        self.pygame.display.update(self.sprites.draw(self.screen))
        
    def add_entity(self, model_entity_id):
        model_entity=self.model.get_entity(model_entity_id)
        new_sprite=self.Sprite(model_entity)
        self.sprite_from_model[model_entity]=new_sprite
        self.sprites.add(new_sprite)
        
    def delete_entity(self, model_entity_id):
        model_entity=self.model.get_entity(model_entity_id)
        delete_sprite=self.sprite_from_model[model_entity]
        del self.sprite_from_model[model_entity]
        self.sprites.remove(delete_sprite)

        
