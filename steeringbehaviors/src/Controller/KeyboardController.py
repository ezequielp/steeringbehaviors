'''
Created on 27/11/2009

@author: Ezequiel N. Pozzo
'''
from Controller import Controller

class BaseKeyboardController(Controller):
    def __init__(self, event_handler):
        Controller.__init__(event_handler)
        self.modifiers=set('SHIFT','CAPS','ALT')
        
        self.keys=set(['F'+str(x) for x in range(12)])
        +set(map(chr, range(ord('a'), ord('z'))))
        +set(['Esc', 'Space', 'Enter'])
        +set(map(chr, range(ord('0'), ord('9'))))
        '''TODO: more keys'''
        self.registered_keys=dict()
        self._key_codes=dict()
        
        
    def register_event_type(self, key, action):
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
        action:
            DOWN
            UP
            
        Instantiate and print self.modifiers and self.keys for more.
        '''
        assert action in ['DOWN', 'UP'], "Action must be UP or DOWN"
        
        modifiers=self.modifiers
        keys=self.keys
        used_modifiers=set()
        
        import string
        key=string.split(key, '-')
        
        if len(key)==1:
            assert len(key[0])==1 or isinstance(key[0], chr), "Wrong key format."
        for m in key[0:-1]:
            assert m in modifiers-used_modifiers, "Token error: "+m
            used_modifiers.add(string.capitalize(m))
            
       
        
        if key[-1] in keys:
            used_key=key[-1]
        else:
            assert (len(key[-1])==1 and key[-1][0] in keys), "Token error:"+key[-1]
            used_key=key[-1][0]
            
        key_name='-'.join(sorted(used_modifiers))+str(used_key)
        
        try:
            return self._key_codes[key_name]
        except KeyError:
            type_id=self._key_codes[key_name]=self.event_handler.new_event_type()
            self.binded_types[type_id]=used_modifiers, used_key, action
            
            return type_id
            
class PygameKeyboardController(object):
    '''
    Implementation of keyboard controller using pygame.
    '''

    def __init__(self, event_handler):
        '''
        Constructor
        '''
        BaseKeyboardController.__init__(self, event_handler)
        import pygame
        pygame.init()
        
        self._pyg=pygame
        
        self._pyg_key_lookup= {
            pygame.
        }
        
        
    def register_event_type(self, key, action):
        type_id=BaseKeyboardController.register_event_type(self, key, action)
        used_modifiers, used_key, action=self.binded_types[type_id]
        
        
        #Creates a quick lookup table to handle pygame events
        self._id_of_pyg_evet[pyg_event]=type_id
        

    def update(self, event):
        output_events=[]
        pygame=self._pyg
        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
            action=event.type
        
        