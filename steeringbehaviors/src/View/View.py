'''
Created on 16/11/2009

@author: Ezequiel N. Pozzo
Edited by JuanPi Carbajal
Last edit: Wednesday, November 18 2009
'''
from __future__ import division
import numpy as np
from Tools import real2pix as rp
import config

# Colormap
from colormap import *


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
        
    def update(self):
        # Here sprites are updated. How? Idea: apply the transformation
        # self._project.transformation(Model.actors) or something like that.
        # 
        pass     
 

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
    
 
    
    def set_transform(self,move=np.array([0,0]), 
                           rotate=np.array([0]),
                           scale=np.array([1,1])):
        self._project.set_transform(move, rotate, scale)
        

    def get_world_position(self, view_position):
        '''
        Returns the position in world coordinates for the 
        point view_position
        '''
        return self._project.inverse_transform(view_position)


    def get_entity_at(self, view_position):
        '''
        Returns the entity id at the requested position or None if there isn't any.
        '''
        assert False, "Not implemented"

class TopDownSprite(object):
    '''
    A sprite for a top down view.
    '''
    def __init__(self, image, image_angle):
        self.set_sprite_for_orientation(image, image_angle)
        self._sprite=dict()
        self.image=image
        
    def set_sprite_for_orientation(self, image, angle_from_vertical):
        self._image=image
        self._initial_angle=angle_from_vertical
        
    def allow_angles(self, N):
        '''
        Set the sprite to allow N orientation angles in the interval [0, 360)
        It is better to call this at initialization phase.
        '''
        self._N=N
        for i in range(N):
            angle=i*360.0/N+self._initial_angle
            self._sprite[i]=self.get_rotated_image(self._image, angle)
            
    
    def set_orientation(self, angle):
        
        i=round(((angle-self._initial_angle)*self._N*1.0/360)) % self._N
        
        #print angle, self._initial_angle, self._N, i
        self.image=self._sprite[i]
    
class PygameViewer(View2D):
    '''
    A class rendering the actors of the Model into a Pygame window
    '''        
    from pygame.sprite import Sprite as SpriteParent
    import pygame
    
    def __init__(self, Model):
        View2D.__init__(self, Model)

        pygame=self.pygame
        self.pygsprites=pygame.sprite
        
        pygame.init()
        
        self.Sprite._project=self._project
        
        self._sprites=pygame.sprite.RenderUpdates()
        self._untraced_sprites=pygame.sprite.RenderUpdates()
        self._traced_sprites=pygame.sprite.RenderUpdates()

        self._clock=pygame.time.Clock()
        
        from weakref import WeakKeyDictionary
        self.sprite_from_model=WeakKeyDictionary()
        
        '''
        Starts a simple black screen.        TODO: improve to be configurable        '''
        self.screen=pygame.display.set_mode(config.screen_size)
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(tuple(cmap[ckey['w']]))
        self.background=background
        self.screen.blit(background, (0,0))
        pygame.display.flip()


    class Sprite(SpriteParent, TopDownSprite):
        def __init__(self, model_entity,shape='o',size=3,color='k'):
            '''
            @model_entity_position: the position of the model object. Use [position] to get reference!!!
            '''
            pygame=PygameViewer.pygame
            PygameViewer.SpriteParent.__init__(self)
            
            self.model=model_entity
            
            self.rect=pygame.Rect(self._project.transform(model_entity.position)
                                  , (size,size))
            
            '''
            TODO: continue refactoring imaging capabilities to TopDownSprite
            '''
            self._draw_entity(shape,size,color)
            
            TopDownSprite.__init__(self, self.original_image, 0)
            #If the shape is a circle, ignore rotation angles
            if shape!='o':
                self.allow_angles(72)
            else:
                self.allow_angles(1)
            

            
        def update(self):
            PygameViewer.SpriteParent.update(self)
            
            self.set_orientation(-self.model.ang*57.296)
            self.rect=self.image.get_rect()
            self.rect.center=self._project.transform(self.model.position)
            
        def get_rotated_image(self, image, angle):
            from pygame import transform
            return transform.rotate(image, angle)
            
        def _draw_entity(self,shape='o',size=3,color='k'):
            '''
               Draws entity following arguments.
               shape:
                    'o' - circle
                    's' - square
               color:
                   Can be a color key
                   'k' - black
                   'w' - white
                   'r' - red
                   'g' - green
                   'b' - blue
                   
                   or a tuple eith r,g,b values [0,255]
                   
                   TODO: still dirty
            '''  
            if type(color)==type(str()):
                color=tuple(cmap[ckey[color]])
               
            simple_sprite=PygameViewer.pygame.Surface((2*size,2*size))
            simple_sprite.fill(tuple(cmap[ckey['w']]))
            simple_sprite.set_colorkey(tuple(cmap[ckey['w']]),
                                                  PygameViewer.pygame.RLEACCEL)
            self.original_image=simple_sprite
            
            if shape=='o':
                PygameViewer.pygame.draw.circle(self.original_image, color,
                                                              (size,size), size)
            elif shape=='s':
                PygameViewer.pygame.draw.rect(self.original_image,color,(.5*size,
                                                     .5*size,1.5*size,1.5*size))
                
            
        
    def on_update(self, event):
        self.update()
        
    def update(self):
        #self.pygame.event.pump()

        self._untraced_sprites.clear(self.screen, self.background)
        
        self._sprites.update()
        
        self.pygame.display.update(self._traced_sprites.draw(self.screen))

        self.pygame.display.update(self._untraced_sprites.draw(self.screen))
        
        
    def add_entity(self, model_entity_id, trace=False, color='k', shape='o',
                   size=3):
        model_entity=self.model.get_entity(model_entity_id)
        new_sprite=self.Sprite(model_entity,shape,size,color)
        
        self.sprite_from_model[model_entity]=new_sprite
        self._sprites.add(new_sprite)
        if trace:
            self._traced_sprites.add(new_sprite)
        else:
            self._untraced_sprites.add(new_sprite)
        
    def delete_entity(self, model_entity_id):
        model_entity=self.model.get_entity(model_entity_id)
        
        delete_sprite=self.sprite_from_model[model_entity]
        del self.sprite_from_model[model_entity]
        self._sprites.remove(delete_sprite)
        if delete_sprite in self._untraced_sprites:
            self._untraced_sprites.remove(delete_sprite)

    def get_entity_at(self, view_position, size=(10,10)):
        pygsprites=self.pygsprites
        pos_sprite=pygsprites.Sprite()
        pos_sprite.rect=self.pygame.Rect(view_position, size)
        pos_sprite.rect.center=view_position
        try:
            return pygsprites.spritecollide(pos_sprite, self._sprites, False)[0].model
        except IndexError:
            return None
            
    def get_colliding_entities(self, entity_id):
        '''
        TODO: Move to the model when it supports shapes
        '''
        sprite=self.sprite_from_model[self.model.get_entity(entity_id)]
        colliding_sprites=self.pygsprites.spritecollide(sprite, self._sprites, False)

        try:
            return [sprite.model.id for sprite in colliding_sprites if sprite.model.id!=entity_id]
        except TypeError:
            return None
        
        
        
        
