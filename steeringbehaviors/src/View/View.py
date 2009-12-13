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
import os
path = os.path.dirname(__file__)

# Colormap
from colormap import *
PERIODIC_HACK=False
DEFAULT_FONT="JuraDemiBold.ttf"

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
        # It is not really private. You can still access it if you have an instance of the obj
        # But it is private to the child I think.
        #self._sprites=np.array([])
        self._project=rp.Transformation()
        self._n_of_entities=0
        self.entities=dict()
        self.using_background=False
 
    
    def set_transform(self,move=np.array([0,0]), 
                           rotate=np.array([0]),
                           scale=np.array([1,1])):
        self._project.set_transform(move, rotate, scale)
        
    def camera_center(self, new_center):
        self.set_transform(move=self.screen_center-new_center)
        self.background.scroll_to(new_center)
        
    def get_world_position(self, view_position):
        '''
        Returns the position in world coordinates for the 
        point view_position
        '''
        return self._project.inverse_transform(view_position)

    def get_view_position(self, world_position):
        '''
        Returns the position in world coordinates for the 
        point view_position
        '''
        return self._project.transform(world_position)

    def get_entity_at(self, view_position):
        '''
        Returns the entity id at the requested position or None if there isn't any.
        '''
        assert False, "Not implemented"
        
    def add_entity(self, model_entity_id, trace=False, color='k', shape='o',
                   size=3):
        assert False, "Not implemented"
        
    def delete_entity(self, model_entity_id):  
        assert False, "Not implemented"
        
    def add_text_entity(self, text, position , font=None, size=10,color=(0,0,0)):
        '''
        Adds text with top left corner located at position.
        If font is None, default font will be used.
        Size is in view units. 
        
        returns: View entity entity id
        '''
        assert False, "Not implemented"
    def delete_text_entity(self, id):
        assert False, "Not implemented"

   
    def move_entity(self, view_entity_id, new_pos):
        '''
        Moves entity given by view_entity_id to new_pos
        
        To move a model entity use the model.
        
        '''
        assert False, "Not implemented"

    def change_text_entity(self, entity_id, new_text):
        '''
        Changes text to new_text
        '''
        assert False, "Not implemented"
       
    def add_view_entity(self, entity):
        eid=self._n_of_entities
        self._n_of_entities+=1
        self.entities[eid]=entity
        return eid
        
    def delete_view_entity(self, eid):
        del self.entities[eid]
    
    def get_view_entity(self, eid):
        return self.entities[eid]
    
    def set_background(self, background_entity):
        self.background=background_entity
        self.using_background=True
    
    
class BackgroundEntity(object):
    '''
    A background manager entity. 
    '''
    def __init__(self, zero_position=(0,0)):
        self.zero_position=zero_position
        self.has_changed=True
        self.render_offset=zero_position
        
    def scroll_to(self, new_position):
        scroll=new_position-self.zero_position
        self.scroll(*scroll)
        
    
        
        
class PygSimpleBackground(BackgroundEntity):
    '''
    Background entity ready to be used with a pygame view
    '''
    def __init__(self, image,zero_position=(0,0)):
        '''
        image must be a pygame surface
        '''
        BackgroundEntity.__init__(self, zero_position)
        
        real_siz=image.get_size()
        self._real_size=real_siz
        self._virtual_size=(real_siz[0]*2, real_siz[1]*2)
        
        from pygame import Surface, Rect
        v_i=self._virtual_image=Surface(self._virtual_size)
        v_i.blit(image, (0,0))
        v_i.blit(image, (real_siz[0],0))
        v_i.blit(image, (0,real_siz[1]))
        v_i.blit(image, (real_siz[0],real_siz[1]))
        
        viewport=Rect(zero_position, real_siz)
        self._vp=viewport
        self.image=self._virtual_image.subsurface(viewport)
        
    def scroll(self, dx, dy):
        viewport=self._vp
        vsize=viewport.size
        vpos=self.zero_position
        
        viewport.topleft=((vpos[0]+dx)%vsize[0], (vpos[1]+dy)%vsize[1])
        self.image=self._virtual_image.subsurface(viewport)
        self.has_changed=True
        
        
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
    
    def __init__(self, Model, background=None, fullscreen=False):
        View2D.__init__(self, Model)

        pygame = self.pygame
        self.pygsprites = pygame.sprite
        
        pygame.init()
        
        self.Sprite._project = self._project
        
        self._sprites = pygame.sprite.RenderUpdates()
        self._untraced_sprites = pygame.sprite.RenderUpdates()
        self._traced_sprites = pygame.sprite.RenderUpdates()

        self._clock = pygame.time.Clock()
        
        from weakref import WeakKeyDictionary
        self.sprite_from_model = WeakKeyDictionary()
        
        '''
        Starts a simple black screen.        TODO: improve to be configurable        '''
        if fullscreen:
            fs=pygame.FULLSCREEN
        else:
            fs=0
        self.screen = pygame.display.set_mode(config.screen_size, fs)
        self.screen_center=(config.screen_size[0]*1.0/2, config.screen_size[1]*1.0/2)
        
        if background==None:
            self.set_background(self.get_dummy_background())
        
        self.screen.blit(self.background.image, (0,0))

        pygame.display.flip()

    def get_dummy_background(self):
        from pygame.draw import circle
        from pygame import image
        from pygame.transform import scale
        
        filename=os.path.join(path, "Images", "1144.jpg")

        sc_size=self.screen.get_size()
        background=image.load(filename)
        background=scale(background, sc_size).convert()
        '''background = self.pygame.Surface(sc_size)
        background = background.convert()
        background.fill(tuple(cmap[ckey['k']]))
        
        for i in range(1000):
            x=randint(0, sc_size[0])
            y=randint(0, sc_size[1])
            circle(background, tuple(cmap[ckey['w']]), (x,y), 1)'''
        
        background_entity=PygSimpleBackground(background, zero_position=(sc_size[0]/2, sc_size[1]/2))

        return background_entity
        

    class Sprite(SpriteParent, TopDownSprite):
        def __init__(self, model_entity,shape='o',size=3,color='k'):
            '''
            @model_entity_position: the position of the model object. Use [position] to get reference!!!
            '''
            pygame=PygameViewer.pygame
            PygameViewer.SpriteParent.__init__(self)
            
            self.model = model_entity
            
            self.rect = pygame.Rect(
                self._project.transform(model_entity.position), 
                                  (size,size))
            
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
            
            if PERIODIC_HACK:
                pos= self.rect.center
                self.rect.center=(pos[0]%config.screen_size[0],pos[1]%config.screen_size[1])
            
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
                
            
      
    def get_screen_center(self):
        return self.screen_center  
    
    def on_update(self, event):
        self.update()
        
    def update(self):
        #self.pygame.event.pump()
        self._sprites.update()
        
        if self.background.has_changed:
            self.background.has_changed=False
            self.screen.blit(self.background.image, (0,0))
            
            self.pygame.display.update(self._traced_sprites.draw(self.screen))
            self.pygame.display.update(self._untraced_sprites.draw(self.screen))
            self.pygame.display.flip()
        else:
            
            self._untraced_sprites.clear(self.screen, self.background.image)
            
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
     
    def delete_text_entity(self, eid):
        text_sprite=self.get_view_entity(eid)
        text_sprite.kill()
        self.delete_view_entity(eid)
        
    def add_text_entity(self, text, position , filename=None, size=10, color=(0,0,0)):
        '''
        Adds text with top left corner located at position.
        If filename is None, default font will be used.
        Size is in view units. 
        
        returns: View entity entity id
        '''
        import os
        from pygame import font, sprite
        
        if filename==None:
            filename=os.path.join(path, "Font", DEFAULT_FONT)
        
        font=font.Font(filename, size)
        rendered_text=font.render(text, True, color)
        
        text_sprite=sprite.Sprite()
        text_sprite.image=rendered_text
        text_sprite.rect=rendered_text.get_rect()
        text_sprite.rect.topleft=position
        text_sprite.font=font
        text_sprite.color=color
        self._sprites.add(text_sprite)
        self._untraced_sprites.add(text_sprite)

        return self.add_view_entity(text_sprite)

    def change_text_entity(self, entity_id, new_text):
        old_text=self.get_view_entity(entity_id)
        position=old_text.rect.topleft
        try:
            new_image=old_text.font.render(new_text, True, old_text.color)
        except TypeError:
            new_image=old_text.font.render(str(new_text), True, old_text.color)
        old_text.image=new_image
        old_text.rect=new_image.get_rect()
        old_text.rect.topleft=position

    def get_new_id(self):
        self.view_ids+=self.view_ids
        return self.view_ids
    
    def move_entity(self, view_entity_id, new_pos):
        '''
        Moves entity given by view_entity_id to new_pos
        
        To move a model entity use the model.
        
        '''
        sprite=self.get_view_entity(view_entity_id)
        sprite.rect.topleft=new_pos
   
        
        
