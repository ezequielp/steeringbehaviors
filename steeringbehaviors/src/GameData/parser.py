from xml.sax.handler import ContentHandler
from xml.sax import parse

class Dispatcher:

    def dispatch(self, prefix, name, attrs=None):
        # Build the call to the correspoding method or the default
        
        # Method Name
        mname = prefix + name.capitalize()
        
        # Default Method Name
        dname = 'default' + prefix.capitalize()
        
        method = getattr(self, mname, None)
        
        # If the method is there use it, if nt use the default
        if callable(method): args = ()
        else:
            method = getattr(self, dname, None)
            args = name,

        if prefix == 'start': args += attrs,

        if callable(method): method(*args)

    def startElement(self, name, attrs):
        self.dispatch('start', name, attrs)
        
    def endElement(self, name):
        self.dispatch('end', name)

class SVGParser(Dispatcher, ContentHandler): 
    def __init__(self):
        ContentHandler.__init__(self)
        self.layers_count = 0
        
    def startG(self, attrs):
        if 'layer' in attrs['id']:
            self.layers_count +=1
            print attrs.keys()
    def endG(self):
        pass
        
    def startDefault(self,attrs):
        pass

    def endDefault(self):
        pass
    
layers=SVGParser()
parse('Player_demo.svg',layers)

print 'There are ', layers.layers_count, ' layers in the document' 
