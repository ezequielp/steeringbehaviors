'''
Monday, December 28 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Monday, December 28 2009
'''

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


