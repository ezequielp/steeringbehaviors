from View.View import PygameViewer
from Model.Model import PhysicsModel
from Controller.MouseController import PygameMouseController
from Mediator.EventManager import EventManager
from Controller.MiscControllers import PygCPUSpinner
from steering.behaviors import SteerForSeek, SteerForArrive, SteerForPursuit
import random
from numpy import pi


FPS=30 #Same FPS for all for the moment

class PursuitTestApp():

    def __init__(self, event_handler, world, screen, mouse, spinner, keyboard):
        self.event_handler=event_handler
        self.world=world
        self.screen=screen
        self.mouse=mouse
        self.spinner=spinner
        self.keyboard=keyboard
        
        self.steering_entities=set()
        self.entity_list=[self.world.add_entity((100,100),(100, 0)) for i in xrange(1)]
        [self.screen.add_entity(entity, trace=False,color='b',size=5) for entity in self.entity_list]
        [self.world.apply_relative_force(entity, pi/2, 100) for entity in self.entity_list]
       
        self.AddSteeringEntity(SteerForSeek)
        self.AddSteeringEntity(SteerForArrive)
        self.AddSteeringEntity(SteerForPursuit)

        event_handler.bind(self.on_mouse_left_up, mouse.MOUSE_BTN3_UP) #Left click ends app
        for listener_obj in [self.mouse, self.world, self.screen, self.keyboard ]:
            event_handler.bind(listener_obj.on_update, self.spinner.TICK)
		
    def AddSteeringEntity(self, Behavior):
        spinner=self.spinner
        #Create and apply Seeking Behavior controller to entity
        seeking_entity=self.world.add_entity((200,200),(0, 0))
        self.screen.add_entity(seeking_entity, trace=False,size=3,color='r')
        seek=Behavior(self.world, seeking_entity)
        seek.target_entity(self.entity_list[0])
        self.steering_entities.add(seek)
        
        self.event_handler.bind(seek.update, spinner.TICK)

    def run(self):
    	self.spinner.run()

    def on_mouse_left_up(self, event):
		self.spinner.stop()    	
		
if __name__ == '__main__':
	event_handler=EventManager()
	world=PhysicsModel()
	screen=PygameViewer(world)
	mouse=PygameMouseController(event_handler)
	spinner=PygCPUSpinner(FPS, event_handler)	
	
	python_app=PursuitTestApp(event_handler, world, screen, mouse, spinner)	
	python_app.run()
       




