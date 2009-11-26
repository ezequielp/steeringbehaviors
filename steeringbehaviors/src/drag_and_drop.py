from View.View import PygameViewer
from Model.Model import PhysicsModel
from Controller.MouseController import PygameMouseController
from Mediator.EventManager import EventManager
from Controller.MiscControllers import PygCPUSpinner

FPS=30 #Same FPS for all for the moment

class DragAndDropApp():
	
	def __init__(self, event_handler, world, screen, mouse, spinner):
		self.event_handler=event_handler
		self.world=world
		self.screen=screen
		self.mouse=mouse
		self.spinner=spinner
		
		#entitylist=[world.add_entity((400*(i/20.0),200*(i%3)), (0,0)) for i in xrange(0,3)]
		#[screen.add_entity(entity) for entity in entitylist]

		event_handler.bind(self.on_mouse_down, mouse.MOUSE_BTN1_DOWN)
		event_handler.bind(self.on_mouse_up, mouse.MOUSE_BTN1_UP)
		event_handler.bind(self.on_mouse_move, mouse.MOUSE_MOVE)
		event_handler.bind(self.on_mouse_left_up, mouse.MOUSE_BTN3_UP) #Left click ends app
		for listener_obj in [self.mouse, self.world, self.screen ]:
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
			
	def on_mouse_left_up(self, event):
		self.spinner.stop()
		
	def run(self):
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
	spinner=PygCPUSpinner(FPS, event_handler)	
	
	python_app=DragAndDropApp(event_handler, world, screen, mouse, spinner)	
	python_app.run()
			
		
