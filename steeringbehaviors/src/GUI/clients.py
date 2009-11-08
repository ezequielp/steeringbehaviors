'''
Created on 08/11/2009

@author: Guille
'''
from GUI.config import client, screen_size

if client=="standalone":
    import pygame
    from pygame import event  
    from pygame import locals
    from pygame.sprite import RenderUpdates
    
   
    
    class Client(object):
        '''
        classdocs
        '''
        
        def __init__(self):
            '''
            Constructor
            '''
            pygame.init()
            self.sprites=RenderUpdates()

        def add_actors(self, actors):
            self.sprites.add(actors)
            
        
                
                
        def run(self):
            screen=pygame.display.set_mode(screen_size)
            background = pygame.Surface(screen.get_size())
            background = background.convert()
            background.fill((250, 250, 250))
            screen.blit(background, (0,0))
            pygame.display.flip()
            quit=False
            
            clock=pygame.time.Clock(
                                )
            while not quit:
                dt=clock.tick(30)
                events=event.get()
                for ev in events:
                    if ev.type==locals.QUIT:
                        quit=True
                self.sprites.clear(screen, background)
                self.sprites.update(dt)
                
                pygame.display.update(self.sprites.draw(screen))
            