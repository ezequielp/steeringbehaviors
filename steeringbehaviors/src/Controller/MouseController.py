'''
Created on Monday, November 23 2009

@author: JuanPi Carbajal
Edited by Ezequiel N. Pozzo
Last edit: Tuesday, November 24 2009
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
        self._EH=EventManager
        self.last_btn=[False, False, False]
        
    def update(self): 
        #Pygame - Event handling
        #int_event={"Type":[], "Pos":[],"BTN":[]}
        output_events=[]
        pygame=self.pygame
        btn=self.last_btn

        # get events that happened in this frame
        for event in pygame.event.get([pygame.MOUSEMOTION, 
                                pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]):
            int_event=dict()
            # Mouse
            if pygame.mouse.get_focused(): 
                # Buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos=event.pos
                    if event.button == 1:
                        typ=self.MOUSE_BTN1_DOWN
                        btn[0]=True
                    elif event.button == 2:
                        typ=self.MOUSE_BTN2_DOWN
                        btn[1]=True                                      
                    elif event.button == 3:
                        typ=self.MOUSE_BTN3_DOWN
                        btn[2]=True 
                    else:
                        assert False, str(event.button)   
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos=event.pos
                    if event.button == 1:
                        typ=self.MOUSE_BTN1_UP
                        btn[0]=False
                    elif event.button == 2:
                        typ=self.MOUSE_BTN2_UP
                        btn[1]=False                                      
                    elif event.button == 3:
                        typ=self.MOUSE_BTN3_DOWN
                        btn[2]=False    
                    else:
                        assert False, str(event.button)   
                # Motion
                elif event.type == pygame.MOUSEMOTION:
                    pos=event.pos
                    btn=[but==1 for but in event.buttons]
                    typ=self.MOUSE_MOVE
                else:
                    assert False, str(event)
          
                # Set Event dict
                int_event["Type"]=typ
                int_event["Pos"]=pos
                int_event["BTN"]=btn
                output_events.append(int_event)
                
        self.last_btn=btn
        self._EH.post(output_events)
        return True
        