'''
Created on 11/12/2009

@author: Ezequiel N. Pozzo
'''

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
        
    def set_text(self, text):
        try:
            text_id=self.text_id
        except AttributeError:
            self.create_label(text)
            return
        self.view.change_text_entity(text_id, text)
        
    def create_label(self, text):
        self.text_id=self.view.add_text_entity(text, size=self.font_size, color=self.color)
        
    def update(self, event):
        try:
            self.view.change_
        except AttributeError:
            assert False, "Label not initiated!"
            