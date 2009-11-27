'''
Created on 25/11/2009

@author: Ezequiel
'''
class Controller(object):
    '''
    Abstract controller
    '''
    def __init__(self, EventManager):
        self.event_handler=event_handler