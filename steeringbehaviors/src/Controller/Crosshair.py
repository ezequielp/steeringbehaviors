'''
Created on 28/11/2009

@author: Ezequiel N. Pozzo
'''
from Controller import Controller

class Crosshair(Controller):
    '''
    A simple 
    '''


    def __init__(self, view, world_model, event_handler):
        '''
        Constructor
        '''
        Controller.__init__(self, event_handler)
        self.view=view
        self.world=world_model
        
        #registers sprite
        view.add_entity()
        
    #Callbacks for mouse controller
    def mouse_move_cb(self, event):
        position=event['Pos']
        