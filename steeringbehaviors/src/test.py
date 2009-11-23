'''
Created on 07/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Monday, November 23 2009
'''
def loop(model, view, time):
    timer=0
    while timer<time:
            dt=view.update(fps)
            model.update(dt)        
            timer+=dt
            
# Test all the functions from the class PygameViewer
if __name__ == '__main__':
    from Model.Model import PhysicsModel
    from View.View import PygameViewer
    from Mediator.EventManager import EventManager
    from Controller.MouseController import PygameMouseController
    
    model=PhysicsModel()     # Model
    view=PygameViewer(model) # Viewer
    eh=EventManager()    # Event Manager
    
    entitylist=[model.add_entity((400*(i/20.0),200*(i%3)), (0,0)) for i in xrange(0,20)]
    [view.add_entity(entity) for entity in entitylist]
    timer=0.0
    last_done=0
    fps=30
    dt=0.0
    idpop=[]
    
    
    print "Testing dynamic add/remove entities from view"
    while timer<3000:
        dt=view.update(fps)
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
    print "...OK"   
    
    print "Restarting model and view"
    for entity_id in entitylist:
        view.delete_entity(entity_id)
        model.delete_entity(entity_id)

    print "...OK"
            
    print "Testing random free movement"
    import random
    
    entity_list=[model.add_entity((random.randint(160,480),random.randint(120, 360)),(random.randint(-100,100), random.randint(-100, 100) )) for i in xrange(20) ]
    [view.add_entity(entity, trace=True) for entity in entitylist]
    
    loop(model, view, 1000)
    
    print "...OK"
            
    print "Restarting model and view"
    for entity_id in entitylist:
        view.delete_entity(entity_id)
        model.delete_entity(entity_id)
    print "...OK"
            
    print "Testing random forced movement"
    entity_list=[model.add_entity((random.randint(160,480),random.randint(120, 360)),(random.randint(-100,100), random.randint(-100, 100) )) for i in xrange(20) ]
    [view.add_entity(entity, trace=True) for entity in entitylist]
    [model.apply_force(entity, (random.randint(-50, 50), random.randint(-50, 50))) for entity in entitylist]
        
    loop(model, view, 1000)
    print "...OK"

    print "Testing Mouse control: Move the mouse and press the buttons"
    def mousePos(pos):
        print pos
       
    mouse=PygameMouseController(eh)
    eh.bind(mousePos,mouse.MOUSE_MOVE)
    eh.bind(mousePos,mouse.MOUSE_BTN1_DOWN)
    eh.bind(mousePos,mouse.MOUSE_BTN1_UP)

    eventcount=0
    
    while eventcount<30:
        if mouse.update():
            eventcount+=1
        dt=view.update(20)
        model.update(dt)
          
    print "...OK"
    print "Remaining queue:"
    print '\n'.join([mouse.pygame.event.event_name(event.type) for event in mouse.pygame.event.get()])
   
    print "All test OK, be happy!"    
