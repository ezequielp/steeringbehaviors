from Controller.Steering.SteerForFlock import SteerForFlock

import random as rnd
from numpy import pi,round


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
       
        self.add_in_square(SteerForFlock)
        #self.AddSteeringEntity(SteerForFlock,number=10,color='g')
        #self.AddSteeringEntity(SteerForFlock,number=6,color='r')
        
        #Left click ends app
        event_handler.bind(self.on_mouse_left_up, mouse.MOUSE_BTN3_UP)
         
        for listener_obj in [self.mouse, self.world, self.screen, self.keyboard ]:
            event_handler.bind(listener_obj.on_update, self.spinner.TICK)
            
    def AddSteeringEntity(self, Behavior,number=1,color='r'):
      
        #Create and apply Seeking Behavior controller to entity
        for i in xrange(1,number,1):
            pos=round((rnd.uniform(100,400),rnd.uniform(100,400)))
            seeking_entity=self.world.add_entity(pos,(0, 0))
            #I commented this because I didn't knew why it was there...
            #self.world.apply_relative_force(seeking_entity, pi/2, (2*(i%2)-1)*200)
            self.screen.add_entity(seeking_entity, trace=False,size=5,color=color, shape='s')
            flock=Behavior(self.world, seeking_entity)
            self.steering_entities.add(flock)
            self.event_handler.bind(flock.update, self.spinner.TICK)

    def add_in_square(self, Behavior, color='r', shape='s'):
        side=50.0
        for pos in [(side,side),(2*side,side),(side,2*side),(2*side,2*side)]:
            seeking_entity=self.world.add_entity(pos,(100.0,100.0))
            self.screen.add_entity(seeking_entity, trace=False,size=8,color=color, shape=shape)
            flock=Behavior(self.world, seeking_entity)
            self.steering_entities.add(flock)
            self.event_handler.bind(flock.update, self.spinner.TICK)
            
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
    python_app=FlockTestApp(event_handler, world, screen, mouse, spinner, keyboard)	
    python_app.run()
       




