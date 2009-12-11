'''
Created on 11/12/2009

@author: Ezequiel N. Pozzo
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
        self.text_id=self.view.add_text_entity(text, self.view.get_view_position(self.model.get_position(self.follow_entity_id))+offset,size=self.font_size, color=self.color)
        
    def update(self, event):
        try:
            self.view.move_entity(self.text_id, offset+self.view.get_view_position(self.model.get_position(self.follow_entity_id)))
        except AttributeError:
            assert False, "Label not initiated!"
            