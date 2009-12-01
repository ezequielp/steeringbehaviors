'''
Created on 28/11/2009

@author: Ezequiel N. Pozzo
'''
from Controller import Controller

class Crosshair(Controller):
    '''
    A simple 
    '''

    crosshair_damage=10
    def __init__(self, view, world_model, event_handler):
        '''
        Constructor
        '''
        Controller.__init__(self, event_handler)
        self.view=view
        self.world=world_model
        #registers sprite on model and view. Grabs it to disallow physics modification
        ch_id=world_model.add_entity((0,0), (0,0))
        view.add_entity(ch_id, shape='s')
        world_model.grab_entity(ch_id)

        self.ch_id=ch_id
        
        self.DAMAGE_EVENT=world_model.DAMAGE_EVENT
        
        
    #Callback for mouse controller
    def mouse_move_cb(self, event):
        position=event['Pos']
        view_transform=self.view.get_world_position
        old_position=self.world.get_position(self.ch_id)
        
        self.world.move_entity(self.ch_id, view_transform(position))
        
    #Firing event
    def fire_cb(self, event):
        damaged_entities=self.view.get_colliding_entities(self.ch_id)
        
        for hitted_id in damaged_entities:
            self.event_handler.post({'Type': self.DAMAGE_EVENT, 'Damage': self.crosshair_damage, 'Damaged entity':  hitted_id, 'Damaging entity': self.ch_id})
            
        
            
    def get_entity_id(self):
        return self.ch_id