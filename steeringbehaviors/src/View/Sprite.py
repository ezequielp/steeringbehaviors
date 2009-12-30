'''
Monday, December 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Monday, December 28 2009
'''
from pygame.sprite import Sprite as SpriteParent
import pygame

# Colormap
from colormap import *
PERIODIC_HACK=False

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

# Sprite #################################################
class Sprite(SpriteParent, TopDownSprite):
    def __init__(self, model_entity,shape='o',size=3,color='k',image=None):
        '''
        @model_entity_position: the position of the model object. Use [position] to get reference!!!
        '''
        SpriteParent.__init__(self)
        
        self.original_image = None
        
        self.model = model_entity
        
        self.rect = pygame.Rect(
            self._project.transform(model_entity.position), 
                                (size,size))
        
        '''
        TODO: continue refactoring imaging capabilities to TopDownSprite
        '''
        if image:
            self._draw_avatar_entity(image)
        else:
            self._draw_entity(shape,size,color)
        
        # Where is self.orinigal:image defined?
        TopDownSprite.__init__(self, self.original_image, -90)

        #If the shape is a circle, ignore rotation angles
        if shape!='o' or image:
            self.allow_angles(144)
        else:
            self.allow_angles(1)
        

        
    def update(self):
        SpriteParent.update(self)
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
            
        simple_sprite=pygame.Surface((2*size,2*size))
        simple_sprite.fill(tuple(cmap[ckey['w']]))
        simple_sprite.set_colorkey(tuple(cmap[ckey['w']]),
                                                pygame.RLEACCEL)
        self.original_image=simple_sprite
        
        if shape=='o':
            pygame.draw.circle(self.original_image, color,
                                                            (size,size), size)
        elif shape=='s':
            pygame.draw.rect(self.original_image,color,(.5*size,
                                                    .5*size,1.5*size,1.5*size))

    def _draw_avatar_entity(self,image):
        # Load the sprite
        self.original_image = pygame.image.load(image).convert_alpha()
                                                    
##################################################                

