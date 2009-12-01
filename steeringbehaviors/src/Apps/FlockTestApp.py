from Controller.Steering.SteerForFlock import SteerForFlock
import random as rnd
from numpy import pi


FPS=30 #Same FPS for all for the moment

class FlockTestApp():
    def __init__(self, event_handler, world, screen, mouse, spinner, keyboard):
        self.event_handler=event_handler
        self.world=world
        self.screen=screen
        self.mouse=mouse
        self.spinner=spinner
        self.keyboard=keyboard
        
        self.steering_entities=set()
       
        self.AddSteeringEntity(SteerForFlock,number=10,color='g')
        self.AddSteeringEntity(SteerForFlock,number=6,color='r')
        
        #Left click ends app
        event_handler.bind(self.on_mouse_left_up, mouse.MOUSE_BTN3_UP)
         
        for listener_obj in [self.mouse, self.world, self.screen, self.keyboard ]:
            event_handler.bind(listener_obj.on_update, self.spinner.TICK)
            
    def AddSteeringEntity(self, Behavior,number=1,color='r'):
        spinner=self.spinner
        
        #Create and apply Seeking Behavior controller to entity
        for i in xrange(1,number,1):
            pos=(rnd.uniform(0,240),rnd.uniform(0,320))
            seeking_entity=self.world.add_entity(pos,(0, 0))
            self.screen.add_entity(seeking_entity, trace=False,size=3,color=color)
            flock=Behavior(self.world, seeking_entity)
            self.steering_entities.add(flock)
            self.event_handler.bind(flock.update, spinner.TICK)

    def run(self):
        self.spinner.run()

    def on_mouse_left_up(self, event):
        self.spinner.stop()    	

if __name__ == '__main__':
    from View.View import PygameViewer
    from Model.Model import PhysicsModel
    from Controller.MouseController import PygameMouseController
    from Mediator.EventManager import EventManager
    from Controller.MiscControllers import PygCPUSpinner
    from Controller.KeyboardController import PygameKeyboardController
    
    event_handler=EventManager()
    world=PhysicsModel(event_handler)
    screen=PygameViewer(world)
    mouse=PygameMouseController(event_handler)
    spinner=PygCPUSpinner(FPS, event_handler)	
    keyboard=PygameKeyboardController(event_handler)
    python_app=PursuitTestApp(event_handler, world, screen, mouse, spinner, keyboard)	
    python_app.run()
       




