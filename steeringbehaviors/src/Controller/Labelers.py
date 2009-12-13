'''
Created on 11/12/2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last Edit: Saturday, December 12 2009
'''
offset=(-20,20)
class ConstantLabel(object):
    '''
    A label that displays always the same text over an entity
    '''


    def __init__(self, model, view, follow_entity_id, view_size=10, color=(0,0,0)):
        '''
        follow_entity_id is the entity to follow
        view_size is the font size in view units
        
        '''
        self.view, self.model=view, model
        self.follow_entity_id=follow_entity_id
        self.font_size=view_size
        self.color=color
        self.on_update=self.update
        
    def __del__(self):
        self.view.delete_text_entity(self.text_id)
        
        
    def set_text(self, text):
        try:
            text_id=self.text_id
        except AttributeError:
            self.create_label(text)
            return
        self.view.change_text_entity(text_id, text)
        
    def create_label(self, text):
        self.text_id=self.view.add_text_entity(text, 
                         self.view.get_view_position(
                         self.model.get_position(self.follow_entity_id))+offset,
                         size=self.font_size, color=self.color)
        
    
    def update(self, event):
        try:
            self.view.move_entity(self.text_id, 
            offset+self.view.get_view_position(
                                self.model.get_position(self.follow_entity_id)))
        except AttributeError:
            assert False, "Label not initiated!"
            
class DynamicLabel(ConstantLabel):
    def __init__(self, model, view, follow_entity_id, 
                   view_size=10, color=(0,0,0), getter_callback_function=False):
        ConstantLabel.__init__(self, model, view, follow_entity_id, view_size,
                                                                          color)
        if getter_callback_function:
            self.set_getter_callback(getter_callback_function)
        
    def set_getter_callback(self, function):
        '''
        Function must accept model_id as parameter and return a representable
        object to use as label
        '''
        self._cb_function=function
        
    def update(self, event):
        text=self._cb_function(self.follow_entity_id)
        
        self.set_text(text)
            
        ConstantLabel.update(self, event)
