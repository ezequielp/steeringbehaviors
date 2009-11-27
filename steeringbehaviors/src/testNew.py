'''
Test using new functionalities
Created on Wednesday, November 25 2009

@author: JuanPi Carbajal
Last edit: Wednesday, November 25 2009
'''
# Test all the functions from the class PygameViewer

from View.View import PygameViewer
from Model.Model import PhysicsModel
from Controller.MouseController import PygameMouseController
from Mediator.EventManager import EventManager
from Controller.MiscControllers import PygCPUSpinner
from numpy import pi
from steering.behaviors import SteerForPursuit
FPS=30 #Same FPS for all for the moment



class Test():

    def __init__(self, event_handler, world, screen, mouse, spinner):
        self.event_handler=event_handler
        self.world=world
        self.screen=screen
        self.mouse=mouse
        self.spinner=spinner
        self.steering_entities=set()
        self.prepareWorld()
        
    
    def run(self):
        self.RestartModelView()
        self.AddRemoveEntities()
        self.RandomMove()
        from steering.behaviors import SteerForSeek, SteerForArrive, SteerForPursuit
        
        self.AddSteeringEntity(SteerForSeek)
        self.AddSteeringEntity(SteerForArrive)
        self.AddSteeringEntity(SteerForPursuit)
        self.DragNDrop()
        
    def prepareWorld(self):
        model=self.world
        view=self.screen
        import random
        entity_list=[model.add_entity((100,100),(100, 0)) for i in xrange(1) ]
        [view.add_entity(entity, trace=False) for entity in entity_list]
        [model.apply_relative_force(entity, pi/2, 100) for entity in entity_list]
        self.entity_list=entity_list
        
        
    def AddSteeringEntity(self, Behavior):
        spinner=self.spinner
        #Create and apply Seeking Behavior controller to entity
        seeking_entity=self.world.add_entity((200,200),(0, 0))
        self.screen.add_entity(seeking_entity, trace=False)
        seek=Behavior(self.world, seeking_entity)
        seek.target_entity(self.entity_list[0])
        self.steering_entities.add(seek)
        
        self.event_handler.bind(seek.update, spinner.TICK)
        
        #Misc Binds
        #for listener_obj in [self.mouse, self.world, self.screen ]:
        #    event_handler.bind(listener_obj.on_update, self.spinner.TICK)
            
        #self.event_handler.bind(spinner.stop, self.mouse.MOUSE_BTN1_UP)
        #self.spinner.run()
        
      
    def AddRemoveEntities(self):
        print "Testing dynamic add/remove entities from view"
        '''
        while timer<3000:
              dt=view.update()
              print dt.__class__
              model.update(dt)
              # add and delete entities
              if timer>=last_done+100 and len(entitylist)>0:
                 idpop.insert(len(idpop),entitylist.pop())
                 view.delete_entity(idpop[-1])
                 last_done=timer
           
            if len(entitylist)==0:
                entitylist.extend(idpop)
                [view.add_entity(entity) for entity in entitylist]
                idpop=[]
      
        timer+=dt
        '''
        print "...OK"   
        
    def RestartModelView(self):
        print "Restarting model and view"
        '''
        for entity_id in entitylist:
            view.delete_entity(entity_id)
            model.delete_entity(entity_id)

        
    '''
        print "...OK"
       
    def RandomMove(self):
        print "Testing random free movement"
        '''
        import random
        entity_list=[model.add_entity((random.randint(160,480),random.randint(120, 360)),(random.randint(-100,100), random.randint(-100, 100) )) for i in xrange(20) ]
        [view.add_entity(entity, trace=True) for entity in entitylist]
        loop(model, view, 1000)
    '''
        print "...OK"
        
    def DragNDrop(self):
        '''
        Test mouse for Drag and Drop
        '''
        from Apps.drag_and_drop import DragAndDropApp
        test=DragAndDropApp(event_handler, world, screen, mouse, spinner)	
        test.run()
        
    
 
if __name__ == '__main__':
    event_handler=EventManager()
    world=PhysicsModel()
    screen=PygameViewer(world)
    mouse=PygameMouseController(event_handler)
    spinner=PygCPUSpinner(FPS, event_handler)	
    
    python_app=Test(event_handler, world, screen, mouse, spinner)	
    python_app.run()
