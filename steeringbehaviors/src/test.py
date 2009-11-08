'''
Created on 07/11/2009

@author: Ezequiel N. Pozzo
'''

if __name__ == '__main__':
    from steering import behaviors
    from GUI import actors
    from GUI.clients import Client
    
    client=Client()
    
    #Defines a simple npc and a sprite controled by the mouse
    actorA=actors.BasicActor((300,300))
    actorB=actors.MouseActor()
    
    #The npc follows the mouse with a seek behavior
    actorA.setTarget(actorB, behaviors.steerForSeek)
    
    client.add_actors([actorA, actorB])
    client.run()