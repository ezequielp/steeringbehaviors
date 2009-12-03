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
        self._custom_ticks=dict()
        self._custom_ticks[fps]=event_handler.new_event_type()
        
    def run(self):
        assert False, "Abstract Class, use specific implementation instead"
        
    def ticks_at_frequency(self, fps):
        try:
            return self._custom_ticks[fps]
        except KeyError:
            self._custom_ticks[fps]=self.event_handler.new_event_type()
            return self._custom_ticks[fps]
        
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
        
        
        
    def run(self, total_time=None):
        '''
        total_time is time in seconds to keep ticking
        '''
        eh=self.event_handler
        TICK=self.TICK
        self.running=True
        if total_time!=None:
            current_time=0
            
        dt=1.0/self.fps
        while self.running:
            '''TODO: Multifps ticking'''
            self.pygame.event.pump()
            self.clock.tick(self.fps)*1.0/1000
            
            eh.post({'Type': TICK, 'dt': dt})
            if total_time!=None:
                current_time+=dt
                
                if current_time>total_time:
                    self.stop()
            
            
    def stop(self):
        self.running=False
        
