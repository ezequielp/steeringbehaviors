'''
Created on 27/11/2009

@author: Ezequiel N. Pozzo
'''
from Controller import Controller

class BaseKeyboardController(Controller):
    def __init__(self, EventHandler):
        Controller.__init__(EventHandler)
    def attach_key_binding(self, key, callback):
        '''
        key: 
        string indicating binding:
        (Shift/Ctrl/Alt -)LETTER 
        or single character:
        LETTER
        Example:
        Ctrl-Alt-S
        Alt-Enter
        Enter
        Instanciate and print self.modifiers and self.keys for more.
        '''
        self.modifiers=set('SHIFT','CAPS','ALT')
        self.keys=set(['F'+str(x) for x in range(12)])
        +set(map(chr, range(ord('a'), ord('z'))))
        +set(['Esc', 'Space', 'Enter'])
        +set(map(chr, range(ord('0'), ord('9'))))
        +set( map(str, range(ord('0'), ord('9'))))
        possible_keys=self.keys
        import string
        key=string.split(key, '-')
        
        if len(key)==1:
            assert len(key[0])==1, "Wrong key format."
        
            

    def attach_concrete(self, key_code, callback):
        assert False, "Implement"

class PygameKeyboardController(object):
    '''
    Implementation of keyboard controller using pygame.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        