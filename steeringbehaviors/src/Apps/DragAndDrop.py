from View.View import PygameViewer
from Model.Model import PhysicsModel
from Controller.MouseController import PygameMouseController
from Mediator.EventManager import EventManager
from Controller.MiscControllers import PygCPUSpinner
from Controller.KeyboardController import PygameKeyboardController

FPS=30 #Same FPS for all for the moment

class DragAndDropApp():
	
	def __init__(self, event_handler, world, screen, mouse, spinner, keyboard):
		self.event_handler=event_handler
		self.world=world
		self.screen=screen
		self.mouse=mouse
		self.spinner=spinner
		self.keyboard=keyboard
		
		
		event_handler.bind(self.on_mouse_down, mouse.MOUSE_BTN1_DOWN)
		event_handler.bind(self.on_mouse_up, mouse.MOUSE_BTN1_UP)
		event_handler.bind(self.on_mouse_move, mouse.MOUSE_MOVE)
		event_handler.bind(self.on_quit, mouse.MOUSE_BTN3_UP) #Left click ends app
		
		space_key_event_id=keyboard.register_event_type('Right Ctrl-Q', 'UP') #Ctrl-Q ends app too
		
		event_handler.bind(self.on_quit, space_key_event_id)
		for listener_obj in [self.mouse, self.world, self.screen, self.keyboard ]:
			event_handler.bind(listener_obj.on_update, self.spinner.TICK)
			
		
		
		self.grabbed=None
		
	def on_mouse_down(self, event):
		entity=self.screen.get_entity_at(event['Pos'])
		if entity!=None:
			self.grabbed=entity.id
			self.world.grab_entity(entity.id)
			
	def on_mouse_up(self, event):
		if self.grabbed!=None:
			self.world.drop_entity(self.grabbed)
			self.grabbed=None
			
	def on_mouse_move(self, event):
		if self.grabbed!=None:
			self.world.move_entity(self.grabbed, self.screen.get_world_position(event['Pos']))
			
	def on_quit(self, event):
		
		self.spinner.stop()
		
	def run(self):
		'''
		App will not return from Run until the spinner is stopped, so be sure to bind an event to 
		self.spinner.stop()
		'''
		
		self.spinner.run()
	
if __name__ == '__main__':
	event_handler=EventManager()
	world=PhysicsModel(event_handler)
	screen=PygameViewer(world)
	mouse=PygameMouseController(event_handler)
	spinner=PygCPUSpinner(FPS, event_handler)	
	keyboard=PygameKeyboardController(event_handler)
	
	python_app=DragAndDropApp(event_handler, world, screen, mouse, spinner, keyboard)	
	python_app.run()
			
		
