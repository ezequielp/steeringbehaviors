'''
Created on 14/11/2009

@author: Ezequiel N. Pozzo
TODO: create some events.
'''

from Tools.orderedset import OrderedSet as orderedset

class EventManager(object):
    '''This object will mediate most communication between model, view and controller
   
    
    '''
    from Tools.WeakRefSet import WeakMethod


    def __init__(self):
        '''
        WeakKeyDictionary allows the Garbage collector to delete the listener objects if 
        all other references are lost.
        '''
        self._registered_events=0
        self.listeners = dict()
        self.ALL_EVENTS=self.new_event_type()
        
    def new_event_type(self):
        self.listeners[self._registered_events]=orderedset()
        self._registered_events+=1
        return self._registered_events-1
    
    def bind(self, listener, event_type=None):
        '''
        Registers an event listener. 
        @listener Function that will receive events. Must have one parameter (event).
        @event_type The type of events the listener will hear, default: Hears all.
        '''
        if event_type==None:
            event_type=self.ALL_EVENTS
            
        
        self.listeners[event_type].add(self.WeakMethod(listener))
        
       
    def unbind(self, listener, type=None):
        '''
        Detaches listener from all types of events or from a specific type or from all types
        '''
        if type!=None:
            self.listeners[type].remove(listener)
            return
            
        for type in self.get_type():
            self.listeners[type].remove(listener)
        
    def post(self, event):
        '''
        Sends event to all listeners
        
        Event must be an event or a list
        TODO: decouple posting and actual delivery of events (Add instant priority too)
        '''
        
        if not isinstance(event, list):
            type=event['Type']
            
            for listener in self.listeners[type]:
                listener(event)
        else:
            for ev in event:
                type=ev['Type']
                
                for listener in self.listeners[type]:
                    listener(ev)
        