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
        
        # If the method is there use it, if not use the default
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
        self.LAYER='inkscape:groupmode'
        self.LABEL='inkscape:label'
        self.LINK='xlink:href'
        
        self.__current=dict()
        
        self.view=dict()
        
        #self.layers_count = 0
    
    def startG(self, attrs):
        '''
            Dispatches the different ethods for the different layers
        '''
        if  self.getValue(attrs,self.LAYER):
            self.dispatch('start',self.getValue(attrs,self.LABEL),attrs)
            
    def endG(self):
        if self.__current:
            self.dispatch('end',self.__current["layer"])
            
    def startView(self,attrs):
#        self.__current.update(attrs)
        self.__current.update(layer="View")
        print "Parsing View"
    
    def endView(self):
        self.__current.clear()
        print "Ending View"
        
    def startImage(self,attrs):
        if self.__current['layer'] == "View":
            self.view["avatar"]=attrs[self.LINK][7:] # Erase file://
            
        
    def startController(self,attrs):
        self.__current.update(attrs)
        self.__current.update(layer="Controller")
        print "Parsing Controller"
        
    def endController(self):
        self.__current.clear()
        print "Ending Controller"

    def startModel(self,attrs):
        self.__current.update(attrs)
        self.__current.update(layer="Model")
        print "Parsing Model"
                            
    def endModel(self):
        self.__current.clear()
        print "Ending Model"

    def startDefault(self,attrs):
        pass

    def endDefault(self):
        pass
        
    def getValue(self,attrs,attrname):
        # Search for an attribute name and return value
        if attrname in attrs:
            return attrs[attrname]
        else:
            return None 
         
class Player(object):
    import pygame
    import sys
        
    def __init__(self,player_file):
        self.data=SVGParser()
        parse(player_file,self.data)
        
        
    # Subclass pygame.sprite.Sprite
    class Avatar(pygame.sprite.Sprite):

        def __init__(self, position,image):
            pygame=Player.pygame
            # Call pygame.sprite.Sprite.__init__ to do some internal work
            pygame.sprite.Sprite.__init__(self)

            # Load the stickMan
            self.image = pygame.image.load(image).convert()

            # Create a rectangle
            self.rect = self.image.get_rect()

            # Position the rectangle
            self.rect.x = position[0]
            self.rect.y = position[1]
        
    def draw(self):
        pygame=self.pygame
        sys=self.sys
        pygame.init()
        screen = pygame.display.set_mode((256, 256))
        pygame.display.set_caption('Sprite Example')
        screen.fill((159, 182, 205))

        # Create a Avatar sprite
        character = self.Avatar((screen.get_rect().x, screen.get_rect().y),
                                                       self.data.view["avatar"])

        # Blit the sprite
        screen.blit(character.image, character.rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
    

test=Player('Player_demo.svg') 
test.draw()
   
#layers=SVGParser()
#parse(,layers)
#print 'There are ', layers.layers_count, ' layers in the document' 
