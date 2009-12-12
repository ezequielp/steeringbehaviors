from Controller.Steering.SteerForOffset import SteerForOffset
import random
from numpy import pi


FPS=30 #Same FPS for all for the moment

class OffsetTestApp():
    def __init__(self, event_handler, world, screen, mouse, spinner, keyboard):
        self.event_handler=event_handler
        self.world=world
        self.screen=screen
        self.mouse=mouse
        self.spinner=spinner
        self.keyboard=keyboard
        
        self.steering_entities=[]
        self.entity_list=[self.world.add_entity((320,240),(0,0))]
        self.screen.add_entity(self.entity_list[0], trace=False,size=5,color="g")

        offset1 = self.AddSteeringEntity(SteerForOffset,'g',
                                                      pos=(0,200,),vel=(0,-10,))

        offset2 = self.AddSteeringEntity(SteerForOffset,'r',
                                                      pos=(0,200,),vel=(0,-10,))
        
        self.steering_entities[offset1].target_entity(
                                            self.entity_list[0])
        self.steering_entities[offset1].set_offset(100.0)
        self.steering_entities[offset1].set_side(1.0)
        
        self.steering_entities[offset2].target_entity(
                                            self.entity_list[0])  
        self.steering_entities[offset2].set_offset(100.0)
        self.steering_entities[offset2].set_side(-1.0)       
        
        event_handler.bind(self.on_mouse_left_up, mouse.MOUSE_BTN3_UP) #Left click ends app
        for listener_obj in [self.mouse, self.world, self.screen, self.keyboard ]:
            event_handler.bind(listener_obj.on_update, self.spinner.TICK)
            
    def AddSteeringEntity(self,Behavior,color='r',
    pos=(0.0,0.0,),vel=(0.0,0.0,)):
        spinner=self.spinner
        #Create and apply Seeking Behavior controller to entity
        seeking_entity=self.world.add_entity(pos,vel)
        self.screen.add_entity(seeking_entity, trace=False,size=3,color=color)
        seek=Behavior(self.world, seeking_entity)
        self.steering_entities.append(seek)
        
        self.event_handler.bind(seek.update, spinner.TICK)
        return len(self.steering_entities)-1
        
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
    python_app=OffsetTestApp(event_handler, world, screen, mouse, spinner, keyboard)	
    python_app.run()
       




