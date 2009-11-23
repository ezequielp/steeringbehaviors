'''
Created on Monday, November 23 2009

@author: JuanPi Carbajal
Edited by Ezequiel N. Pozzo
Last edit: Monday, November 23 2009
'''
from __future__ import division
import numpy as np

class Controller(object):
   '''
   Abstract controller
   '''
   def __init__(self,EventManager):
      pass
      
class PygameMouseController(Controller):
    '''
    A Mouse controller
    The tyes have the format
    {'Type': ID, 'Pos': Position (where? in Viewer?)where 
    the event ocurred, 'BTN1': True o False if button 1 is pressed,
    'BTN2' idem, 'BTN3' idem} 
    '''
    import pygame
    import pygame.locals
      
    def __init__(self,EventManager):
        Controller.__init__(self,EventManager)
        
        # Definition of Mouse events
        self.MOUSE_MOVE=EventManager.new_event_type() 
        self.MOUSE_BTN1_DOWN=EventManager.new_event_type() 
        self.MOUSE_BTN2_DOWN=EventManager.new_event_type()
        self.MOUSE_BTN3_DOWN=EventManager.new_event_type()
        self.MOUSE_BTN1_UP=EventManager.new_event_type()
        self.MOUSE_BTN2_UP=EventManager.new_event_type()                          
        self.MOUSE_BTN3_UP=EventManager.new_event_type()                 
        
        self.pygame.init()        
        self.pygame.mouse.set_visible(True)
        self._events=[]
        self._EH=EventManager
        
    def update(self): 
        #Pygame - Event handling
        event={"Type":[], "Pos":[],"BTN":[]}
        pygame=self.pygame
        # get events that happened in this frame
        for event in pygame.event.get():
        
            # Mouse
            if pygame.mouse.get_focused(): 
                # Buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos=event.pos
                    if event.button == LEFT:
                        typ=self.MOUSE_BTN1_DOWN
                        btn[0]=True
                    if event.button == RIGHT:
                        typ=self.MOUSE_BTN2_DOWN
                        btn[1]=True                                      
                    if event.button == MIDDLE:
                        typ=self.MOUSE_BTN3_DOWN
                        btn[2]=True    
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos=event.pos
                    if event.button == LEFT:
                        typ=self.MOUSE_BTN1_UP
                        btn[0]=False
                    if event.button == RIGHT:
                        typ=self.MOUSE_BTN2_UP
                        btn[1]=False                                      
                    if event.button == MIDDLE:
                        typ=self.MOUSE_BTN3_DOWN
                        btn[2]=False    

                # Motion
                elif event.type == pygame.MOUSEMOTION:
                    pos=event.pos
                    btn=list(event.buttons)
          
                # Set Event dict
                event["Type"]=typ
                event["Pos"]=pos
                event["BTN"]=btn
                self._events.append(event)
        
        EH.post(self._events)
        return True
        
