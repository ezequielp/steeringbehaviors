'''
Created on 03/12/2009

@author: Ezequiel N. Pozzo
'''

from View import View2D
default_fields=['position']
class TextOutputView(View2D):
    '''
    View that renders to a text file in CSV
    '''


    def __init__(self, Model, filename):
        '''
        Constructor
        '''
        View2D.__init__(self, Model)
        self.filename=filename
        self.current_time=0
        self.saving_entities=list()
        self.labels=dict()
        self.times=list()
        self.log=list()
        self.saved=False
        self.logging=False

    def add_entity(self, model_entity_id):
        assert not self.logging, "Error, already started logging"
        self.saving_entities.append(model_entity_id)
        
    def configure_entity(self, model_entity_id, label):
        assert not self.logging, "Error, already started logging"
        self.labels[model_entity_id]=label
        
    def set_log_fields(self, log_fields, len_of_field):
        assert not self.logging, "Error, already started logging"
        self.log_fields=tuple(log_fields)
        self.len_of_fields=tuple(len_of_field)
        
    def on_update(self, event):
        try:
            log_fields=self.log_fields
        except AttributeError:
            self.log_fields=default_fields
            log_fields=default_fields
            
        self.logging=True
        self.current_time+=event['dt']
        
        self.times.append(str(self.current_time))
        row=list()
        for ent_id in self.saving_entities:
            entity=self.model.get_entity(ent_id)
            
            def entity_getter(field):
                value=getattr(entity, field)
                try:
                    return list(value)
                except TypeError:
                    return [value,]
            
            #row.append(map(str,sum(map(entity_getter, log_fields), []) ))
            row.append(map(repr,sum(map(entity_getter, log_fields), []) ))
            
        self.log.append(sum(row, []))
        
    def save(self):
        filename=self.filename
        lab=list()
        log=self.log
        
        # Building the Header of the file
        lab=[map('_'.join, zip([x[0]]*x[1], map(str,range(x[1])))) for x in zip(self.log_fields, self.len_of_fields)]

        lab=sum(lab,[])
       
        from itertools import product
        lab=['_'.join(x) for x in product(map(str, self.saving_entities), lab) ]
        
        lab=', '.join(lab)+'\n'

        # Building data string
        data='\n'.join(map(', '.join, log))
        file=open(filename, 'w')
        
        print "Saving..."
        file.write(lab)
        file.write(data)
        print "Done"
