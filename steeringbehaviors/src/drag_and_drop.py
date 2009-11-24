from View.View import PygameViewer
from Model.Model import PhysicsModel
from Controller.MouseController import PygameMouseController
from Mediator.EventManager import EventManager
from Controller.MiscControllers import PygCPUSpinner

FPS=10 #Same FPS for all for the moment

class DragAndDropApp():
	
	def __init__(self, event_handler, world, screen, mouse, spinner):
		self.event_handler=event_handler
		self.world=world
		self.screen=screen
		self.mouse=mouse
		self.spinner=spinner
		
		event_handler.bind(self.on_mouse_down, mouse.MOUSE_BTN1_DOWN)
		event_handler.bind(self.on_mouse_move, mouse.MOUSE_MOVE)
		event_handler.bind(self.on_mouse_left_up, mouse.MOUSE_BTN3_UP) #Left click ends app
		
		for listener_obj in [self.mouse, self.world, self.screen ]:
			event_handler.bind(listener_obj.on_update, self.spinner.TICK)  
			
			
		self.grabbed=None
		
	def on_mouse_down(self, event):
		entity=screen.get_entity_at(event.pos)
		if entity!=None:
			self.grabbed=entity
			self.model.grab_entity(entity)
			
	def on_mouse_up(self, event):
		if self.grabbed!=None:
			self.model.drop_entity(self.grabbed)
			
	def on_mouse_move(self, event):
		if self.grabbed!=None:
			self.model.move_entity(self.grabbed, self.view.get_world_position(event.pos))
			
	def on_mouse_left_up(self):
		self.spinner.stop()
		
	def Run(self):
		'''
		App will not return from Run until the spinner is stopped, so be sure to bind an event to 
		self.spinner.stop() 
		'''
		
		self.spinner.run()
	
if __name__ == '__main__':
	event_handler=EventManager()
	world=PhysicsModel()
	screen=PygameViewer(world)
	mouse=PygameMouseController(event_handler)
	spinner=PygCPUSpinner(FPS)	
	
	python_app=DragAndDropApp(event_handler, world, screen, mouse, spinner)	
			
		