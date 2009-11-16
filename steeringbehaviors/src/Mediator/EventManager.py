'''
Created on 14/11/2009

@author: Ezequiel N. Pozzo
TODO: create some events.
'''

class EventManager(object):
    '''This object will mediate most communication between model, view and controller
   
    
    '''


    def __init__(self):
        '''
        WeakKeyDictionary allows the Garbage collector to delete the listener objects if 
        all other references are lost.
        '''
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        
    def bind(self, listener, event_type=None):
        '''
        Registers an event listener. 
        @listener Object who will receive events. Must implement notify function.
        @event_type The type of events the listener will hear, default: Hears all.
        
        TODO: implement listening to type of events. Assert notify in listener.
        '''
        self.listeners[listener]=True
        
    def unbind(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[listener]
            
    def post(self, event):
        '''
        Sends event to all listeners
        '''
        for listener in self.listeners.keys():
            listener.notify(event)