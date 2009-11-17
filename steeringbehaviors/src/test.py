'''
Created on 07/11/2009

@author: Ezequiel N. Pozzo
'''

if __name__ == '__main__':
    from Model.Model import PhysicsModel
    from View.View import PygameViewer
    
    model=PhysicsModel()
    view=PygameViewer(model)
    
    entity1=model.add_entity((0,0), (10,1))
    view.add_entity(entity1)
    while True:
        view.update()
