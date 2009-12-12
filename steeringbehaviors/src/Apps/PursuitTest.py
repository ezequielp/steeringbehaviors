from Controller.Steering.SteerForFlee import SteerForFlee
from Controller.Steering.SteerForArrive import SteerForArrive
from Controller.Steering.SteerForPursuit import SteerForPursuit
from Controller.Steering.SteerForEvasion import SteerForEvasion
from Controller.Steering.SteerForOffset import SteerForOffset
from Controller.Steering.SteerForTrack import SteerForTrack
import random
from numpy import pi

FPS=40 #Same FPS for all for the moment

class PursuitTestApp():
    def __init__(self, event_handler, world, screen, mouse, spinner, keyboard):
        self.event_handler=event_handler
        self.world=world
        self.screen=screen
        self.mouse=mouse
        self.spinner=spinner
        self.keyboard=keyboard
        
        self.steering_entities=[]
        self.entity_list=[self.world.add_entity((100,100),(100, 0)) for i in xrange(1)]
        [self.screen.add_entity(entity, trace=False,shape='s',color='b',size=5)
                                                 for entity in self.entity_list]
        [self.world.apply_relative_force(entity, pi/2, 100) for entity in
                                                               self.entity_list]
        from Controller.Cameras import FollowCamera
        self.camera=FollowCamera(screen, world)
        self.camera.set_target(self.entity_list[0])
       
        # Seek entites are green
        self.AddSteeringEntity(SteerForPursuit,'g')
        arrive_id = self.AddSteeringEntity(SteerForArrive,color=[0,255,150])
        self.steering_entities[arrive_id].set_slowing_distance(100.0)

        #Evade entities are red
        evade_id = self.AddSteeringEntity(SteerForEvasion,'r')
        self.steering_entities[evade_id].set_safe_distance(5.0)        
        flee_id = self.AddSteeringEntity(SteerForFlee,'r')
        self.steering_entities[flee_id].set_safe_distance(10.0)
        
        #Track entites are Yellow
        yellow=(255,255,1)
        track_id=self.AddSteeringEntity(SteerForTrack,yellow)
        
        offset_id = self.AddSteeringEntity(SteerForOffset,yellow)
        self.steering_entities[offset_id].set_offset(100.0)
        
        #Left click ends app
        event_handler.bind(self.on_mouse_left_up, mouse.MOUSE_BTN3_UP)

        # Debug information
        event_handler.bind(self.on_toggle_id, 
                                 keyboard.register_event_type('i', 'UP'))
                                 
        for listener_obj in [self.mouse, self.world, self.screen, self.keyboard,
                                                                   self.camera]:
            event_handler.bind(listener_obj.on_update, self.spinner.TICK)
            
    def AddSteeringEntity(self, Behavior,color='r',vel=(0.0,0.0,)):
        spinner=self.spinner
        #Create and apply Seeking Behavior controller to entity
        seeking_entity=self.world.add_entity((200,200),vel)
        self.screen.add_entity(seeking_entity, trace=False,size=3,color=color)
        seek=Behavior(self.world, seeking_entity)
        seek.target_entity(self.entity_list[0])
        self.steering_entities.append(seek)
        
        self.event_handler.bind(seek.update, spinner.TICK)
        return len(self.steering_entities)-1
        
    def run(self):
        self.spinner.run()

    def on_mouse_left_up(self, event):
        self.spinner.stop()    	
    
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
            
            for entity in self.steering_entities:
                ent_id=entity.get_slave_id()
                label=DynamicLabel(self.world,self.screen,ent_id,
                                                            color=(255,255,255))
                label.set_getter_callback(pretty_rep)
                self.labels.add(label)
                label.set_text(str(ent_id))
                self.event_handler.bind(label.update, self.spinner.TICK)
                
        else:
            del self.labels
            
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
       




