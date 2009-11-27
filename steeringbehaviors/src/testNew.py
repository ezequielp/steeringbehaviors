'''
Test using new functionalities
Created on Wednesday, November 25 2009

@author: JuanPi Carbajal, Ezequiel N. Pozzo
Last edit: Wednesday, November 25 2009
'''
# Test all the functions from the class PygameViewer

from View.View import PygameViewer
from Model.Model import PhysicsModel
from Controller.MouseController import PygameMouseController
from Mediator.EventManager import EventManager
from Controller.MiscControllers import PygCPUSpinner
#from steering.behaviors import SteerForPursuit

FPS=30 #Same FPS for all for the moment



class Test():

    def __init__(self, EventManager, PhysicsModel, PygameViewer, 
    PygameMouseController, PygCPUSpinner):
        self.prepareWorld(EventManager, PhysicsModel, PygameViewer, 
    PygameMouseController, PygCPUSpinner)
        
    
    def run(self):
        self.prepareWorld(EventManager, PhysicsModel, PygameViewer, 
    PygameMouseController, PygCPUSpinner)
        self.RestartModelView()
        
        self.prepareWorld(EventManager, PhysicsModel, PygameViewer, 
    PygameMouseController, PygCPUSpinner)
        self.AddRemoveEntities()
        
        self.prepareWorld(EventManager, PhysicsModel, PygameViewer, 
    PygameMouseController, PygCPUSpinner)
        self.RandomMove()
        
        self.prepareWorld(EventManager, PhysicsModel, PygameViewer, 
    PygameMouseController, PygCPUSpinner)
        self.DragNDrop()
        
        self.prepareWorld(EventManager, PhysicsModel, PygameViewer, 
    PygameMouseController, PygCPUSpinner)
        self.PursuitTest()

        self.prepareWorld(EventManager, PhysicsModel, PygameViewer, 
    PygameMouseController, PygCPUSpinner)
        self.CombinedTest()
        
    def prepareWorld(self, EventManager, PhysicsModel, PygameViewer, 
    PygameMouseController, PygCPUSpinner):
        self.event_handler=EventManager()
        self.world=PhysicsModel()
        self.screen=PygameViewer(self.world)
        self.mouse=PygameMouseController(self.event_handler)
        self.spinner=PygCPUSpinner(FPS, self.event_handler)	
      
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
        print "Testing Drag and Drop: Pick the circles and move them around"+"\n"+"Right-click to end this test"
        
        from Apps.DragAndDrop import DragAndDropApp
       	self.entitylist=[self.world.add_entity((400*(i/20.0),200*(i%3)), (0,0)) for i in xrange(0,3)]
        [self.screen.add_entity(entity) for entity in self.entitylist]

        test=DragAndDropApp(self.event_handler, self.world, self.screen, 
        self.mouse, self.spinner)	
        test.run()
        print "...OK"

    def PursuitTest(self):
        print "Look how they behave!"+"\n"+"Right-click to end this test"
        from Apps.PursuitTest import PursuitTestApp
        test=PursuitTestApp(self.event_handler, self.world, self.screen, 
        self.mouse, self.spinner)
        test.run()
        print "...OK"
        
    def CombinedTest(self):
        print "Now you can pick them and move them around!"+"\n"+"Right-click to end this test"
        pass
        from Apps.PursuitTest import PursuitTestApp
        test=PursuitTestApp(self.event_handler, self.world, self.screen, 
        self.mouse, self.spinner)
        self.spinner=PygCPUSpinner(FPS, self.event_handler)	
        from Apps.DragAndDrop import DragAndDropApp
        test2=DragAndDropApp(self.event_handler, self.world, self.screen, 
        self.mouse, self.spinner)	
        test.run()
        
        print "...OK"
            
    
 
if __name__ == '__main__':
    python_app=Test(EventManager, PhysicsModel, PygameViewer, PygameMouseController
    , PygCPUSpinner)	
    python_app.run()
