'''
Created on Tuesday, December 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Tuesday, December 29 2009
'''
import sys,os
filepath, filename = os.path.split(os.path.abspath(os.path.dirname(__file__)) )
sys.path.append(filepath)

from Tools.SVGParser import SVGParser,parse
from Tools.LinAlgebra_extra import vector2angle
from numpy import pi,sqrt,dot

FPS=30 #Same FPS for all for the moment

class SVGTestApp():
    def __init__(self, event_handler, world, screen, mouse, spinner, keyboard):
        self.event_handler=event_handler
        self.world=world
        self.screen=screen
        self.mouse=mouse
        self.spinner=spinner
        self.keyboard=keyboard
        
        self.steering_entities=[]
        self.entity_list=[]
        
        # SVG Parser
        self.SVGdata=SVGParser()
        player_file=os.path.join(filepath,'GameData','Player_demo.svg')
        parse(player_file,self.SVGdata)

        # View realted information
        avatar=os.path.join(filepath,'GameData',self.SVGdata.view["avatar"])
        fwdvector=self.SVGdata.view["fwd_dir"]
        #####
        
        # Model Related information
        # Physical properties
        mass=self.SVGdata.model["mass"][0]
        masunits=self.SVGdata.model["mass"][1] 
        #####

        # Kinematical information
        # Initial velocity
        # TODO: Comes from SVG. Where (Intelligence?)??
        v=(50.0,0)
        
        # Initial position
        # TODO: Comes from SVG, Map
        p=(300,300)

        # Initial angle
        # TODO: Comes from SVG, Where (Intelligence?)??
        # Rotate the unit such that tangential velocity an dforward vetor match
        angle = vector2angle(fwdvector,v)
        
        # Initial angular speed
        # TODO: Comes from SVG, Where (Intelligence?)??
        angspeed=0.0
        
        #####

        # Add circling entity
        
        
        # This comes from the Scale of the Game.
        # TODO: Comes form SVG, Map (??)
        scale=0.6        

        self.entity_list.append(self.world.add_entity(position=p,
                                                      velocity=v,
                                                      ang=0.0,
                                                      angspeed=angspeed,
                                                      mass=mass))
        self.screen.add_entity(self.entity_list[0],trace=False,
                                              image=avatar,
                                              angle=angle,size=scale)
                                              
        f=20.0
        # Angular velocity to match spin with orbit
        w=f/(mass*sqrt(dot(v,v)))
        self.world.apply_relative_force(self.entity_list[0], pi/2, f)
        self.world.set_angspeed(self.entity_list[0], w)       
        
        
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
             [self.mouse, self.world, self.screen, self.keyboard]:
            event_handler.bind(listener_obj.on_update, self.spinner.TICK)

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
    python_app=SVGTestApp(event_handler, world, screen, mouse, spinner, keyboard)	
    python_app.run()
       




