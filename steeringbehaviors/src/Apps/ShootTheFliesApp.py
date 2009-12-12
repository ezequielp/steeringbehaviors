'''
Created on 29/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Saturday, December 12 2009
'''
from Controller.Crosshair import Crosshair

class ShootTheFliesApp(object):
    '''
        Shoot the flies!
        Use the mouse to move and space to shoot
        Why space bar? just to showcase the keyboard controller.
    '''

    def __init__(self, world, view, spinner, event_handler, mouse, keyboard):
        
        from Controller.Steering.SteerForOffset import SteerForOffset as Beh

        mouse.hide()
        self.crosshair=Crosshair(view, world, event_handler)
        self.spinner=spinner
        self.view=view
        self.world=world
        
        self.event_handler=event_handler
        
        flies=set()
        for i in range(10):
            flies.add(self.add_steering_entity(Beh, self.crosshair.get_entity_id()))
            
        self.flies=flies
        #self.add_flee_behavior(flies)
            
        event_handler.bind(self.crosshair.mouse_move_cb, mouse.MOUSE_MOVE)
        event_handler.bind(self.crosshair.fire_cb, keyboard.register_event_type('Space', 'UP'))
        event_handler.bind(self.on_quit, keyboard.register_event_type('Left Ctrl-Q', 'DOWN'))
        event_handler.bind(self.on_toggle_id, keyboard.register_event_type('i', 'UP'))
        for listener_obj in [world, view, mouse, keyboard]:
            event_handler.bind(listener_obj.on_update, self.spinner.TICK)
            
        text_entity_id=view.add_text_entity("Shooting app", (0,0), size=20)
        
        
        
    def on_toggle_id(self, event):
        try:
            showing_id=self.showing_id=not self.showing_id
        except AttributeError:
            showing_id=self.showing_id=True
        
        if showing_id:
            from Controller.Labelers import DynamicLabel
            self.labels=set()
            
            def pretty_rep(entity_id):
                return str(self.world.get_entity(entity_id).total_force)
            
            for entity in self.flies:
                
                label=DynamicLabel(self.world, self.view,entity)
                label.set_getter_callback(pretty_rep)
                self.labels.add(label)
                label.set_text(str(entity))
                self.event_handler.bind(label.update, self.spinner.TICK)
                
        else:
            del self.labels
        
        
    def add_flee_behavior(self, group):
        from Controller.Steering.SteerForFlee import SteerForFlee
        import random
        for flie in group:
            second_flie=flie
            while flie==second_flie:
                second_flie=random.randint(0,len(group))
            
            seek=SteerForFlee(self.world,flie)
            seek.target_entity(second_flie)
            self.steering_entities.add(seek)
            self.event_handler.bind(seek.update, spinner.TICK)

                
    def add_steering_entity(self, Behavior, target):
        import random
        spinner=self.spinner
        #Create and apply Seeking Behavior controller to entity
        seeking_entity=self.world.add_entity((random.randint(0,640) ,random.randint(0,480)),(100, 100))
        
        self.view.add_entity(seeking_entity, trace=False,size=8,shape='s',
                                                                      color='r')
        seek=Behavior(self.world, seeking_entity)
        # Only works with Offset
        seek.set_side(-1.0)

        seek.target_entity(target)
        try:
            self.steering_entities.add(seek)
        except:
            self.steering_entities=set()
            self.steering_entities.add(seek)
        
        self.event_handler.bind(seek.update, spinner.TICK)
        return seeking_entity
   
    def run(self):
        self.spinner.run()
        
    def on_quit(self, event):
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
