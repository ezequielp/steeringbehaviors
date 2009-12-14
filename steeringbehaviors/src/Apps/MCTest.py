from Controller.Steering.SteerForMCamouflage import SteerForMC,SteerForMCHeading
import random
from numpy import pi,dot,sqrt

FPS=30 #Same FPS for all for the moment

class MCTestApp():
    def __init__(self, event_handler, world, screen, mouse, spinner, keyboard):
        self.event_handler=event_handler
        self.world=world
        self.screen=screen
        self.mouse=mouse
        self.spinner=spinner
        self.keyboard=keyboard
        
        self.steering_entities=[]
        self.entity_list=[]
        
        # Add circling entity
        v=(50.0,0)
        self.entity_list.append(self.world.add_entity((300,300),v))
        self.screen.add_entity(self.entity_list[0],
                                         trace=False,shape='s',color='b',size=5)
        f=20.0
        w=f/50.0
        self.world.apply_relative_force(self.entity_list[0], pi/2, f)
        self.world.set_angspeed(self.entity_list[0], w)       
        
        # Seek entity
        mc_entity = self.AddSteeringEntity(SteerForMC,'g',(-10,0))
        self.steering_entities[mc_entity].set_gain(160)
        # Not working
#        mch_entity = self.AddSteeringEntity(SteerForMCHeading,'r',(-10,0))
#        self.steering_entities[mch_entity].set_gain(160)
        
        # Camera
        from Controller.Cameras import FollowCamera
        self.camera = FollowCamera(screen, world)
        self.camera.set_target(self.entity_list[0])
#        self.camera.set_target(self.steering_entities[1].entity_id)
        
        #Left click ends app
        event_handler.bind(self.on_mouse_left_up, mouse.MOUSE_BTN3_UP)

        # Space pauses
        event_handler.bind(self.on_pause, 
                                    keyboard.register_event_type('Space', 'UP'))
        # Debug information
        event_handler.bind(self.on_toggle_id, 
                                 keyboard.register_event_type('i', 'UP'))

        # Drag and Drop
        self.grabbed=None
        event_handler.bind(self.on_mouse_down, mouse.MOUSE_BTN1_DOWN)
        event_handler.bind(self.on_mouse_up, mouse.MOUSE_BTN1_UP)
        event_handler.bind(self.on_mouse_move, mouse.MOUSE_MOVE)
                                
        for listener_obj in \
             [self.mouse, self.world, self.screen, self.keyboard, self.camera]:
            event_handler.bind(listener_obj.on_update, self.spinner.TICK)

    ##########        
    # Seeking Entities Methods
    def AddSteeringEntity(self, Behavior,color='r',vel=(0.0,0.0,)):
        spinner=self.spinner

        #Create and apply Seeking Behavior controller to entity
        seeking_entity=self.world.add_entity((0,0),vel)
        self.screen.add_entity(seeking_entity, trace=False,size=3,color=color)
        seek=Behavior(self.world, seeking_entity)
        seek.target_entity(self.entity_list[0])
        self.steering_entities.append(seek)
        
        self.event_handler.bind(seek.update, spinner.TICK)
        return len(self.steering_entities)-1
            
    #############
    # User events methods

    # Drag and Drop
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
    		self.world.move_entity(self.grabbed,
    		                   self.screen.get_world_position(event['Pos']))
			                   
    def on_pause(self, event):
    	self.spinner.pause()

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

    #########
    def run(self):
        self.spinner.run()
            
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
    python_app=MCTestApp(event_handler, world, screen, mouse, spinner, keyboard)	
    python_app.run()
       




