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
        view.add_sprite(ch_id, shape='s')
        self.ch_id
        
        self.DAMAGE_EVENT=world_model.DAMAGE_EVENT
        
        
    #Callback for mouse controller
    def mouse_move_cb(self, event):
        position=event['Pos']
        view_transform=self.view.get_world_position
        self.world.move_entity(self.ch_id, view_transform(position))
        
    #Firing event
    def fire_cb(self, event):
        damaged_entity=self.view.get_colliding_entity(self.ch_id)
        if damaged_entity!=None:
            self.event_handler.Post({'Type': self.DAMAGE_EVENT, 'Damage': self.croshair_damage, 'Damaged entity':  damaged_entity, 'Damaging entity': self.ch_id})
        
        