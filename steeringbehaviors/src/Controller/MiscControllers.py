'''
Created on 24/11/2009

@author: Ezequiel N. Pozzo
'''

class CPUSpinner(object):
    '''
    An abstract clock object that generates ticks at a given FPS.
    '''


    def __init__(self, fps, event_handler):
        '''
        fps is the number of ticks per seconds to emit
        '''
        self.fps=fps
        self.event_handler=event_handler
        self.TICK=event_handler.new_event_type()
        
    def run(self):
        assert False, "Abstract Class, use specific implementation instead"
        
        
class PygCPUSpinner(CPUSpinner):
    '''
    Specific CPUSpinner implementation using pygame
    '''    
    def __init__(self, fps, event_handler):
        CPUSpinner.__init__(self, fps, event_handler)
        import pygame
        self.pygame=pygame
        self.pygame.init()
        self.clock=self.pygame.time.Clock()
        
        
        
    def run(self):
        eh=self.event_handler
        TICK=self.TICK
        self.running=True
        while self.running:
            dt=self.clock.tick(self.fps)
            eh.post({'Type': TICK, 'dt': dt})
            
            
            
    def stop(self):
        self.running=False
        
