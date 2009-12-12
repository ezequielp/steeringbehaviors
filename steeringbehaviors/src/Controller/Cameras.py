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
        from Steering.SteerForPursuit import SteerForPursuit as Steer
        
        arrive_behavior=Steer(self.model, self.center_id)
        arrive_behavior.target_entity(entity_id)
        self.autocenter=arrive_behavior
        
        
    def on_update(self, event):
        self.autocenter.update(event)
        view=self.view
        from numpy import dot
        move_vec=self.model.get_position(self.center_id)
        vel=self.model.get_velocity(self.center_id)
        new_text="[REC] squared velocity: %07d"%(dot(vel,vel),)
        view.change_text_entity(self.LCD_display_id,new_text)

        self.view.camera_center(move_vec)
        