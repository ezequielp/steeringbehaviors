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
        +set(map(chr, range(ord('A'), ord('Z'))))
        +set(['Esc', 'Space', 'Enter'])
        +set(map(chr, range(ord('0'), ord('9'))))
        '''TODO: more keys'''
        self.registered_keys=dict()
        self.key_codes=dict()
        
        
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
        
        #Checks if it is a valid single key
        if len(key)==1:
            assert len(key[0])==1 or isinstance(key[0], chr), "Wrong key format."
        #Checks that all modifiers are correct
        for m in key[0:-1]:
            assert m in modifiers-used_modifiers, "Token error: "+m
            used_modifiers.add(string.capitalize(m))
            
       
        #Stores key if it is valid or rise error
        if key[-1] in keys:
            used_key=key[-1]
        else:
            assert (len(key[-1])==1 and key[-1][0] in keys), "Token error:"+key[-1]
            used_key=key[-1][0]
            
        #Reconstructs the key name using the convention ALLCAPS and sorted modifiers. To make sure 
        #we use a single key
        key_name='-'.join(sorted(used_modifiers))+str(used_key)+str(action)
        
        try:
            return self.key_codes[key_name]
        except KeyError:
            type_id=self.key_codes[key_name]=self.event_handler.new_event_type()
            
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
        
        _pyg_keys=dict()
        _pyg_actions=dict()
        
        #Creates Key translation table
        for char in set(map(chr, range(ord('a'), ord('z'))))+set(map(chr, range(ord('0'), ord('9'))))+ set(map(chr, range(ord('A'), ord('Z')))):
            _pyg_keys[eval("pygame.K_"+str(char))]=char
        
        _pyg_keys[pygame.K_ESCAPE]='ESC'
        _pyg_keys[pygame.K_SPACE]='SPACE'
        _pyg_keys[pygame.K_RETURN]='ENTER'
        
        #Creates modifier translation table
        #Single key modifiers
        self._pyg_modifiers={pygame.KMOD_SHIFT: 'Shift', pygame.KMOD_CTRL: 'Ctrl', pygame.KMOD_ALT: 'Alt'}
       
        #multiple key modifiers
        inverse_mod={'Shift': pygame.KMOD_SHIFT, 'Ctrl': pygame.KMOD_CTRL, 'Alt': pygame.KMOD_ALT }
        
        from itertools import combinations
        for i in [2,3]:
            comb=combinations(inverse_mod.keys(), i)
            for c in comb:
                #Generates the bitwise OR of each combination of pygame modifiers and maps them to local modifiers
                pyg_modifier=reduce(lambda x,y: x | y,  [inverse_mod[name] for name in c] )
                #Generates the local key. Note that combinations returns tuple in lex. order
                local_modifier='-'.join(c)
                #saves in table
                self._pyg_modifiers[pyg_modifier]=local_modifier
            

        
        #Translation table of actions
        _pyg_actions[pygame.KEYDOWN]='DOWN'
        _pyg_actions[pygame.KEYUP]='UP'
        self._pyg_keys=_pyg_keys
        self._pyg_actions=_pyg_actions
        
    def register_event_type(self, key, action):
        type_id=BaseKeyboardController.register_event_type(self, key, action)
        used_modifiers, used_key, action=self.binded_types[type_id]
        
        
        #Creates a quick lookup table to handle pygame events
        self._id_of_pyg_evet[pyg_event]=type_id
        

    def update(self, event):
        output_events=[]
        pygame=self._pyg
        key_codes=self.key_codes
        
        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
            action=self._pyg_actions[event.type]
            try:
                key=self._pyg_keys[event.key]
            except KeyError:
                print "Key not implemented"
                continue
            if event.mod!=0:
                try:
                    modifiers=self._pyg_modifiers[event.mod]
                except KeyError:
                    print "Modifier not implemented"
                    continue
                event_name='-'.join([modifiers,key, action])
            else:
                event_name='-'.join([key, action])
                
            output_events.append({'Type': key_codes[event_name]})
        self.event_handler.post(output_events)
            
        
        