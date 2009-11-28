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
        #registers sprite on model and view. Grabs it to disallow physics modification
        ch_id=world_model.add_entity((0,0), (0,0))
        world_model.grab_entity(ch_id)
        view.add_sprite(ch_id)
        self.ch_id
        
    #Callbacks for mouse controller
    def mouse_move_cb(self, event):
        position=event['Pos']
        view_transform=self.view.get_world_position
        self.world.
        
        