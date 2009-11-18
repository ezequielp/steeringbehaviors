'''
Created on 07/11/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Wednesday, November 18 2009
'''

# Test all the functions from the class PygameViewer
if __name__ == '__main__':
    from Model.Model import PhysicsModel
    from View.View import PygameViewer
    
    model=PhysicsModel()
    view=PygameViewer(model)
    
    entitylist=[model.add_entity((400*(i/20.0),200*(i%3)), (10,1)) for i in xrange(0,20)]
    [view.add_entity(entity) for entity in entitylist]
    timer=0.0
    fps=20
    dt=0.0
    idpop=[]
    while True:
        dt=view.update(fps)
        
        # add and delete entities
        if timer>=1.0 and len(entitylist)>0:
           idpop.insert(len(idpop),entitylist.pop())
           view.delete_entity(idpop[-1])
           timer=0.0
           
        if len(entitylist)==0:
           entitylist.extend(idpop)
           [view.add_entity(entity) for entity in entitylist]
           idpop=[]
      
      
        timer+=dt
