from View.View import PygameViewer
from Model.Model import PhysicsModel
from Controller.MouseController import PygameMouseController
from Mediator.EventManager import EventManager

class App():
	event_handler=EventManager()
	
	world=PhysicsModel()
	screen=PygameViewer(world)
	mouse=PygameMouseController(event_handler)
	def __init__(self):
		