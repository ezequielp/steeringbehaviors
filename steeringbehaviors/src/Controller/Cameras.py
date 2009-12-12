'''
Created on 11/12/2009

@author: Ezequiel N. Pozzo
'''

class FollowCamera(object):
    '''
    A camera that follows a target in the model.
    '''


    def __init__(self, view, model):
        '''
        Constructor
        '''
        self.model=model
        self.view=view
        center=view.get_screen_center()
        self.center_id=model.add_entity(center, (0,0))
        self.LCD_display_id=view.add_text_entity("[REC]", (0, center[1]*1.9), size=20, color=(255,0,0))

        
    def set_target(self, entity_id):
        from Steering.SteerForSeek import SteerForSeek as Steer
        
        arrive_behavior=Steer(self.model, self.center_id)
        arrive_behavior.target_entity(entity_id)
        self.autocenter=arrive_behavior
        
        
    def on_update(self, event):
        self.autocenter.update(event)
        view=self.view
        
        move_vec=self.model.get_position(self.center_id)
        new_text="[REC] position: (%07d , %07d)"%tuple(move_vec)
        view.change_text_entity(self.LCD_display_id,new_text)

        self.view.camera_center(move_vec)
        