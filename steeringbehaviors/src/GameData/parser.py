from xml.sax.handler import ContentHandler
from xml.sax import parse
from re import search

class Dispatcher:

    def dispatch(self, prefix, name, attrs=None):
        # Build the call to the correspoding method or the default
        
        # Method Name
        mname = prefix + name.capitalize()

        # Default Method Name
        dname = 'default' + prefix.capitalize()
        
        method = getattr(self, mname, None)
        
        # If the method is there use it, if not use the default
        if callable(method): args = name,
        else:
            method = getattr(self, dname, None)
            args = name,

        if prefix == 'start': args += attrs,

        if callable(method): method(*args)

    def startElement(self, name, attrs):
#        print name
        self.dispatch('start', name, attrs)
        
    def endElement(self, name):
#        print name,">"
        self.dispatch('end', name)

class SVGParser(Dispatcher, ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.LAYER='inkscape:groupmode'
        self.LABEL='inkscape:label'
        self.LINK='xlink:href'
        
        self.__current=dict(parent=[],element=str(),data=str())
                
        self.view=dict()
        self.model=dict()
        self.controller=dict()
        
        #self.layers_count = 0
    
    # Group Elements ##################
    def startG(self,name, attrs):
        '''
            Dispatches the different methods for the different layers
        '''
        txt=self.getValue(attrs,self.LABEL)
        print txt
        print self.__current["parent"]
        if txt:
            self.dispatch('start',txt,attrs)
        else:
            txt=self.getValue(attrs,"id")
            self.dispatch('start',txt,attrs)
            
    def endG(self,name):
#        print self.__current["parent"]
        self.dispatch('end',self.__current["parent"][-1])
        
    # Default ##################            
    def defaultStart(self,name,attrs):
        self.__current["parent"].append(name)
        print "defaultStart ", name

    def defaultEnd(self,name):
        print "defaultEnd ", self.__current["parent"].pop()
   
    # Leafs: text, image, path ##################                    
    def startImage(self,name,attrs):
        print "Reading image data"
        self.__current.update(element="image")
        if self.__current['parent'][-1] == "View":
            self.view["avatar"]=attrs[self.LINK][7:] # Erase file://

    def endImage(self,name):
        pass
        
    def startText(self,name,attrs):
        pass
    def endText(self,name):
        pass
            
    def startTspan(self,name,attrs):
        self.__current.update(element="tspan")
        self.__current["data"]=""
        
    def endTspan(self,name):
        txt=self.__current["data"]

        if self.__current['parent'][-1]=="Physics":
            print "Reading physics text data"        
            regexp=r'([a-zA-Z]*)(?:\s|=)*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*([a-zA-Z]*)'
            number=search(regexp,txt)
            if number:
                self.model[number.group(1).lower()] = \
                                       (float(number.group(2)), number.group(3))

        if self.__current['parent'][-1]=="Sensors":
            print "Reading sensor text data"
            
        if self.__current['parent'][-1]=="Intelligence":
            print "Reading intelligence text data"
            
                
        self.__current["data"]=""
  
    def startPath(self,name,attrs):
        self.__current.update(element="path")
        self.__current["data"]=""
            
    def endPath(self,name):
        txt=self.__current["data"]
        
        if self.__current['parent'][-1]=="Physics":
            print "Reading physics path data"

        if self.__current['parent'][-1]=="Sensors":
            print "Reading sensor path data"

        if self.__current['parent'][-1]=="CShapes":
            print "Reading collision shapes path data"
            
        if self.__current['parent'][-1]=="Intelligence":
            print "Reading intelligence path data"
                
    def characters(self, string):
        try: 
            self.__current["data"]+=string
        except KeyError:
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

            # Load the sprite
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
