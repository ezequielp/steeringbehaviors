'''
Created on 27/11/2009

@author: Ezequiel N. Pozzo
'''
from Controller import Controller

class BaseKeyboardController(Controller):
    def __init__(self, event_handler):
        Controller.__init__(self, event_handler)
        self.modifiers=set(map(str, ['RIGHT SHIFT','LEFT SHIFT','RIGHT CTRL', 'LEFT CTRL','RIGHT ALT', 'LEFT ALT']))
        
        self.keys=set(['F'+str(x) for x in range(12)]) \
            | set(map(chr, range(ord('A'), ord('Z')))) \
            | set(['ESC', 'SPACE', 'ENTER']) \
            | set(map(chr, range(ord('0'), ord('9'))))
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
                Right Ctrl-Left Alt-S
                Right Alt-Enter
                Enter
        action:
            DOWN
            UP
            
        Instantiate and print self.modifiers and self.keys for more.
        '''
        import string
        action=string.upper(action)
        assert action=='DOWN' or  action=='UP', "Action must be UP or DOWN: "+action
        
        modifiers=self.modifiers
        keys=self.keys
        used_modifiers=set()
        
        key=string.split(key, '-')
        
        #Checks if it is a valid single key
        if len(key)==1:
            assert string.upper(key[0]) in keys, "Wrong key format: "+key
            key_name='-'.join(['NONE', string.upper(key[0]), action])
            
        else:
            #Checks that all modifiers are correct
            for m in key[0:-1]:
                assert string.upper(m) in modifiers-used_modifiers, "Token error: "+string.upper(m)
                    
                used_modifiers.add(string.upper(m))
                
           
            #Stores key if it is valid or rise error
            if key[-1] in keys:
                used_key=key[-1]
            else:
                assert (len(key[-1])==1 and key[-1][0] in keys), "Token error:"+key[-1]
                used_key=key[-1][0]
                
            #Reconstructs the key name using the convention ALLCAPS and sorted modifiers. To make sure 
            #we use a single key
            key_name='-'.join(sorted(used_modifiers)+[str(used_key), string.upper(action)])
            
        #Returns code and generates it if needed
        try:
            return self.key_codes[key_name]
        except KeyError:
            type_id=self.key_codes[key_name]=self.event_handler.new_event_type()
            
            return type_id
            
class PygameKeyboardController(BaseKeyboardController):
    '''
    Implementation of keyboard controller using pygame.
    '''

    def __init__(self, event_handler):
        '''
        Constructor
        '''
        BaseKeyboardController.__init__(self, event_handler)
        import pygame, string
        pygame.init()
        
        self._pyg=pygame
        
        _pyg_keys=dict()
        _pyg_actions=dict()
        
        #Creates Key translation table
        for char in set(map(chr, range(ord('a'), ord('z')))) \
            |set(map(chr, range(ord('0'), ord('9')))):
            _pyg_keys[eval("pygame.K_"+str(char))]=string.upper(char)
        
        _pyg_keys[pygame.K_ESCAPE]='ESC'
        _pyg_keys[pygame.K_SPACE]='SPACE'
        _pyg_keys[pygame.K_RETURN]='ENTER'
        
        #Creates modifier translation table
        #Single key modifiers
        self._pyg_modifiers={pygame.KMOD_RSHIFT: 'RIGHT SHIFT', pygame.KMOD_RCTRL: 'RIGHT CTRL', pygame.KMOD_RALT: 'RIGHT ALT', \
                             pygame.KMOD_LSHIFT: 'LEFT SHIFT', pygame.KMOD_LCTRL: 'LEFT CTRL', pygame.KMOD_LALT: 'LEFT ALT', \
                             pygame.KMOD_NONE: 'NONE'}
       
        #multiple key modifiers
        inverse_mod=dict()
        for key,value in self._pyg_modifiers.iteritems():
            inverse_mod[value]=key
            
        del inverse_mod['NONE']
        #inverse_mod={'Shift': pygame.KMOD_SHIFT, 'Ctrl': pygame.KMOD_CTRL, 'Alt': pygame.KMOD_ALT }
       
        
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
          
        #Mask of available modifiers to apply to incoming events when updating  
        mask=0
        for single_mask in inverse_mod.values():
            mask=mask|single_mask
        self.availables_mask=mask
        
        #Translation table of actions
        _pyg_actions[pygame.KEYDOWN]='DOWN'
        _pyg_actions[pygame.KEYUP]='UP'
        self._pyg_keys=_pyg_keys
        self._pyg_actions=_pyg_actions
        
        # Debug code
        #for pyg, local in self._pyg_modifiers.iteritems():
        #    print pyg, local
   
    def on_update(self, event):
        output_events=[]
        pygame=self._pyg
        key_codes=self.key_codes
        mask=self.availables_mask
        
        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
            action=self._pyg_actions[event.type]
            mod=event.mod&mask
    
            try:
                key=self._pyg_keys[event.key]
            except KeyError:
                print "Key not implemented"
                continue
            if mod!=0:
                try:
                    modifiers=self._pyg_modifiers[mod]
                except KeyError:
                    print "Modifier not implemented: "+str(mod)
                    continue
                event_name='-'.join([modifiers, key, action])
            else:
                event_name='-'.join(['NONE', key, action])
                
            try:
                output_events.append({'Type': key_codes[event_name]})
            except KeyError:
                continue
        self.event_handler.post(output_events)
            
        
        