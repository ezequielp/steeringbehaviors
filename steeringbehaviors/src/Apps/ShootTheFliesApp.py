'''
Created on 29/11/2009

@author: Ezequiel N. Pozzo
'''
from Controller.Crosshair import Crosshair

class ShootTheFliesApp(object):
    '''
        Shoot the flies!
        Use the mouse to move and space to shoot
        Why space bar? just to showcase the keyboard controller.
    '''

    def __init__(self, world, view, spinner, event_handler, mouse, keyboard):
        
        from Controller.Steering.SteerForSeek import SteerForSeek

        mouse.hide()
        self.crosshair=Crosshair(view, world, event_handler)
        self.spinner=spinner
        self.view=view
        self.world=world
        self.event_handler=event_handler
        
        for i in range(10):
            self.add_steering_entity(SteerForSeek, self.crosshair.get_entity_id())
            
        event_handler.bind(self.crosshair.mouse_move_cb, mouse.MOUSE_MOVE)
        event_handler.bind(self.crosshair.fire_cb, keyboard.register_event_type('Space', 'UP'))
        event_handler.bind(self.on_quit, keyboard.register_event_type('Left Ctrl-Q', 'DOWN'))
        
        for listener_obj in [world, view, mouse, keyboard]:
            event_handler.bind(listener_obj.on_update, self.spinner.TICK)
        
        
    def add_steering_entity(self, Behavior, target):
        import random
        spinner=self.spinner
        #Create and apply Seeking Behavior controller to entity
        seeking_entity=self.world.add_entity((random.randint(0,640) ,random.randint(0,480)),(100, 100))
        print seeking_entity
        self.view.add_entity(seeking_entity, trace=False,size=5,shape='o')
        seek=Behavior(self.world, seeking_entity)
        seek.target_entity(target)
        try:
            self.steering_entities.add(seek)
        except:
            self.steering_entities=set()
            self.steering_entities.add(seek)
        
        self.event_handler.bind(seek.update, spinner.TICK)
        
    def run(self):
        self.spinner.run()
        
    def on_quit(self):
        self.spinner.stop()
        
if __name__ == '__main__':
    from View.View import PygameViewer
    from Model.Model import PhysicsModel
    from Controller.MouseController import PygameMouseController
    from Mediator.EventManager import EventManager
    from Controller.MiscControllers import PygCPUSpinner
    from Controller.KeyboardController import PygameKeyboardController
    
    FPS=30
    event_handler=EventManager()
    world=PhysicsModel(event_handler)
    screen=PygameViewer(world)
    mouse=PygameMouseController(event_handler)
    spinner=PygCPUSpinner(FPS, event_handler)
    keyboard=PygameKeyboardController(event_handler)
    
    python_app=ShootTheFliesApp(world,screen, spinner, event_handler, mouse, keyboard)    
    python_app.run()