'''
Created on Tuesday, December 29 2009

@author: Ezequiel N. Pozzo, JuanPi Carbajal
Last edit: Tuesday, December 29 2009

@brief Contains the SVGParser class, also a Player class as example of use.
'''

from xml.sax.handler import ContentHandler
from xml.sax import parse
from re import search as RegSearch
import os
from numpy import array,sqrt,dot

class Dispatcher:
    '''
    Build method calls for the parser.
    Based on the pattern given on the book "Beginning Python: From Novice to
    Professional" by Magnus Lie Hetland, ISBN 1590599829, 9781590599822
    '''
    
    def dispatch(self, prefix, name, attrs=None):
        # Build the call to the correspoding method or the default
        
        # Method Name
        mname = prefix + name.capitalize()
        #print mname
        # Default Method Name
        dname = 'default' + prefix.capitalize()
        
        method = getattr(self, mname, None)
        
        # If the method is there use it, if not use the default
        if callable(method): args = name,
        else:
            method = getattr(self, dname, None)
            args = name,

        #if prefix == 'start': args += attrs,
        args += attrs,
        
        if callable(method): method(*args)

    def startElement(self, name, attrs):
#        print name
        self.dispatch('start', name, attrs)
        
    def endElement(self, name):
#        print name,">"
        self.dispatch('end', name)

class SVGParser(Dispatcher, ContentHandler):
    '''
        This parser reads an SVG and stores the retrieved information
        on the attributes view, model, controller. Note: Maybe is better to avoid
        references to this classes and just have a dcit called retrieved_data.
        The file is given when the parse method is called.
    '''

#    from re import search as RegSearch

    def __init__(self):
        ContentHandler.__init__(self)
        self.LAYER='inkscape:groupmode'
        self.LABEL='inkscape:label'
        self.LINK='xlink:href'
        
        self.__current=dict(parent=[],element=str(),data=str())
                
        self.view=dict()
        self.view["scale"]=1
        self.model=dict()
        self.model["scale"]=1
        self.controller=dict()

# Doesn't work    
#     from xml.sax import parse as SAXparse
#    def parse(self,filename): 
#        self.SAXparse(filename,self)
            
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
            
    def endG(self,name,attrs):
#        print self.__current["parent"]
        self.dispatch('end',self.__current["parent"][-1])
        
    # Default ##################            
    def defaultStart(self,name,attrs):
        self.__current["parent"].append(name)
        print "defaultStart ", name

    def defaultEnd(self,name,attrs):
        print "defaultEnd ", self.__current["parent"].pop()
   
    # Leafs: text, image, path ##################                    
    def startImage(self,name,attrs):
        print "Reading image data"
        self.__current.update(element="image")
        if self.__current['parent'][-1] == "View":
            abspath=attrs[self.LINK][7:] # Erase file://
            basepath, filename = os.path.split(abspath)
            self.view["avatar"]=filename
            
    def endImage(self,name,attrs):
        pass
        
    def startText(self,name,attrs):
        pass
    def endText(self,name,attrs):
        pass
            
    def startTspan(self,name,attrs):
        self.__current.update(element="tspan")
        self.__current["data"]=""
        
    def endTspan(self,name,attrs):
        self.dispatch('read',self.__current['parent'][-1] + 'text',attrs)
        self.__current["data"]=""
  
    def startPath(self,name,attrs):
        self.__current.update(element="path")
        self.__current["data"]=Path(attrs["d"]).d
        
        # If there is a label dispatch
        txt=self.getValue(attrs,self.LABEL)
        if txt :
            self.dispatch('read',txt,attrs)
            
    def endPath(self,name,attrs):
            
        txt=self.__current["data"]
        
        if self.__current['parent'][-1]=="Physics":
            print "Reading physics path data"

        if self.__current['parent'][-1]=="Sensors":
            print "Reading collision sensors path data"            

        if self.__current['parent'][-1]=="CShapes":
            print "Reading collision shapes path data"
            
        if self.__current['parent'][-1]=="Intelligence":
            print "Reading collision intelligence path data"            
        
        self.__current["data"]=""
            
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
            
    # Read functions ##############################
    def readForwardvector(self,name,attrs):
        '''
            The path is assumed ot be be a direction.
            d="M/m xi,yi xf,yf"
        '''
        print "... Reading Forward Vector"
        path = self.__current["data"]
        # Check if final point is relative
        if path[1][2] == True:
            fwd_dir = array([path[1][1]-path[0][1],
                                        path[1][2]-path[0][2]])
        else:
            fwd_dir = array(path[1][1:3])

        fwd_dir = fwd_dir / sqrt(dot(fwd_dir, fwd_dir) )
            
        if self.__current['parent'][-1]=="View":
            self.view["fwd_dir"]=fwd_dir
                        
        if self.__current['parent'][-1]=="Physics":
            self.model["fwd_dir"]=fwd_dir
            
    def readPhysicstext(self,name,attrs):
        '''
            Reads physical data from text fields
        '''    
        txt=self.__current["data"]
        regexp = \
          r'([a-zA-Z]*)(?:\s|=)*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*([a-zA-Z]*)'
        number=RegSearch(regexp,txt)
        if number:
            self.model[number.group(1).lower()] = \
                                       (float(number.group(2)), number.group(3))
        print "... Read Physics data " + number.group(1).lower()
        
    def readSensorstext(self,name,attrs):
        print "Reading sensor text data"
    
    def readIntelligencetext(self,name,attrs):
        print "Reading intelligence text data"        


class Path:
  """
  The following code is adapted from SVGFIG REFERENCE NEEDED
  
  Path represents an SVG path, an arbitrary set of curves and
  straight segments. Unlike SVG("path", d="..."), Path stores
  coordinates as a list of numbers, rather than a string, so that it is
  transformable in a Fig.

  Path(d, attribute=value)

  d                       required        path data
  attribute=value pairs   keyword list    SVG attributes

  See http://www.w3.org/TR/SVG/paths.html for specification of paths
  from text.

  Internally, Path data is a list of tuples with these definitions:

      * ("Z/z",): close the current path
      * ("H/h", x) or ("V/v", y): a horizontal or vertical line
        segment to x or y
      * ("M/m/L/l/T/t", x, y, global): moveto, lineto, or smooth
        quadratic curveto point (x, y). If global=True, (x, y) should
        not be transformed.
      * ("S/sQ/q", cx, cy, cglobal, x, y, global): polybezier or
        smooth quadratic curveto point (x, y) using (cx, cy) as a
        control point. If cglobal or global=True, (cx, cy) or (x, y)
        should not be transformed.
      * ("C/c", c1x, c1y, c1global, c2x, c2y, c2global, x, y, global):
        cubic curveto point (x, y) using (c1x, c1y) and (c2x, c2y) as
        control points. If c1global, c2global, or global=True, (c1x, c1y),
        (c2x, c2y), or (x, y) should not be transformed.
      * ("A/a", rx, ry, rglobal, x-axis-rotation, angle, large-arc-flag,
        sweep-flag, x, y, global): arcto point (x, y) using the
        aforementioned parameters.
      * (",/.", rx, ry, rglobal, angle, x, y, global): an ellipse at
        point (x, y) with radii (rx, ry). If angle is 0, the whole
        ellipse is drawn; otherwise, a partial ellipse is drawn.
  """
  defaults = {}

  def __repr__(self):
    return "<Path (%d nodes) %s>" % (len(self.d), self.attr)

  def __init__(self, d=[], **attr):
    if isinstance(d, basestring): self.d = self.parse(d)
    else: self.d = list(d)

    self.attr = dict(self.defaults)
    self.attr.update(attr)

  def parse_whitespace(self, index, pathdata):
    """Part of Path's text-command parsing algorithm; used internally."""
    while index < len(pathdata) and pathdata[index] in (" ", "\t", "\r", "\n", ","): index += 1
    return index, pathdata

  def parse_command(self, index, pathdata):
    """Part of Path's text-command parsing algorithm; used internally."""
    index, pathdata = self.parse_whitespace(index, pathdata)

    if index >= len(pathdata): return None, index, pathdata
    command = pathdata[index]
    if "A" <= command <= "Z" or "a" <= command <= "z":
      index += 1
      return command, index, pathdata
    else: 
      return None, index, pathdata

  def parse_number(self, index, pathdata):
    """Part of Path's text-command parsing algorithm; used internally."""
    index, pathdata = self.parse_whitespace(index, pathdata)

    if index >= len(pathdata): return None, index, pathdata
    first_digit = pathdata[index]

    if "0" <= first_digit <= "9" or first_digit in ("-", "+", "."):
      start = index
      while index < len(pathdata) and ("0" <= pathdata[index] <= "9" or pathdata[index] in ("-", "+", ".", "e", "E")):
        index += 1
      end = index

      index = end
      return float(pathdata[start:end]), index, pathdata
    else: 
      return None, index, pathdata

  def parse_boolean(self, index, pathdata):
    """Part of Path's text-command parsing algorithm; used internally."""
    index, pathdata = self.parse_whitespace(index, pathdata)

    if index >= len(pathdata): return None, index, pathdata
    first_digit = pathdata[index]

    if first_digit in ("0", "1"):
      index += 1
      return int(first_digit), index, pathdata
    else:
      return None, index, pathdata

  def parse(self, pathdata):
    """Parses text-commands, converting them into a list of tuples.
    Called by the constructor."""
    output = []
    index = 0
    while True:
      command, index, pathdata = self.parse_command(index, pathdata)
      index, pathdata = self.parse_whitespace(index, pathdata)

      if command == None and index == len(pathdata): break  # this is the normal way out of the loop
      if command in ("Z", "z"):
        output.append((command,))

      ######################
      elif command in ("H", "h", "V", "v"):
        errstring = "Path command \"%s\" requires a number at index %d" % (command, index)
        num1, index, pathdata = self.parse_number(index, pathdata)
        if num1 == None: raise ValueError, errstring

        while num1 != None:
          output.append((command, num1))
          num1, index, pathdata = self.parse_number(index, pathdata)

      ######################
      elif command in ("M", "m", "L", "l", "T", "t"):
        errstring = "Path command \"%s\" requires an x,y pair at index %d" % (command, index)
        num1, index, pathdata = self.parse_number(index, pathdata)
        num2, index, pathdata = self.parse_number(index, pathdata)

        if num1 == None: raise ValueError, errstring

        while num1 != None:
          if num2 == None: raise ValueError, errstring
          output.append((command, num1, num2, False))

          num1, index, pathdata = self.parse_number(index, pathdata)
          num2, index, pathdata = self.parse_number(index, pathdata)

      ######################
      elif command in ("S", "s", "Q", "q"):
        errstring = "Path command \"%s\" requires a cx,cy,x,y quadruplet at index %d" % (command, index)
        num1, index, pathdata = self.parse_number(index, pathdata)
        num2, index, pathdata = self.parse_number(index, pathdata)
        num3, index, pathdata = self.parse_number(index, pathdata)
        num4, index, pathdata = self.parse_number(index, pathdata)

        if num1 == None: raise ValueError, errstring

        while num1 != None:
          if num2 == None or num3 == None or num4 == None: raise ValueError, errstring
          output.append((command, num1, num2, False, num3, num4, False))

          num1, index, pathdata = self.parse_number(index, pathdata)
          num2, index, pathdata = self.parse_number(index, pathdata)
          num3, index, pathdata = self.parse_number(index, pathdata)
          num4, index, pathdata = self.parse_number(index, pathdata)
          
      ######################
      elif command in ("C", "c"):
        errstring = "Path command \"%s\" requires a c1x,c1y,c2x,c2y,x,y sextuplet at index %d" % (command, index)
        num1, index, pathdata = self.parse_number(index, pathdata)
        num2, index, pathdata = self.parse_number(index, pathdata)
        num3, index, pathdata = self.parse_number(index, pathdata)
        num4, index, pathdata = self.parse_number(index, pathdata)
        num5, index, pathdata = self.parse_number(index, pathdata)
        num6, index, pathdata = self.parse_number(index, pathdata)
        
        if num1 == None: raise ValueError, errstring

        while num1 != None:
          if num2 == None or num3 == None or num4 == None or num5 == None or num6 == None: raise ValueError, errstring

          output.append((command, num1, num2, False, num3, num4, False, num5, num6, False))

          num1, index, pathdata = self.parse_number(index, pathdata)
          num2, index, pathdata = self.parse_number(index, pathdata)
          num3, index, pathdata = self.parse_number(index, pathdata)
          num4, index, pathdata = self.parse_number(index, pathdata)
          num5, index, pathdata = self.parse_number(index, pathdata)
          num6, index, pathdata = self.parse_number(index, pathdata)

      ######################
      elif command in ("A", "a"):
        errstring = "Path command \"%s\" requires a rx,ry,angle,large-arc-flag,sweep-flag,x,y septuplet at index %d" % (command, index)
        num1, index, pathdata = self.parse_number(index, pathdata)
        num2, index, pathdata = self.parse_number(index, pathdata)
        num3, index, pathdata = self.parse_number(index, pathdata)
        num4, index, pathdata = self.parse_boolean(index, pathdata)
        num5, index, pathdata = self.parse_boolean(index, pathdata)
        num6, index, pathdata = self.parse_number(index, pathdata)
        num7, index, pathdata = self.parse_number(index, pathdata)

        if num1 == None: raise ValueError, errstring

        while num1 != None:
          if num2 == None or num3 == None or num4 == None or num5 == None or num6 == None or num7 == None: raise ValueError, errstring

          output.append((command, num1, num2, False, num3, num4, num5, num6, num7, False))

          num1, index, pathdata = self.parse_number(index, pathdata)
          num2, index, pathdata = self.parse_number(index, pathdata)
          num3, index, pathdata = self.parse_number(index, pathdata)
          num4, index, pathdata = self.parse_boolean(index, pathdata)
          num5, index, pathdata = self.parse_boolean(index, pathdata)
          num6, index, pathdata = self.parse_number(index, pathdata)
          num7, index, pathdata = self.parse_number(index, pathdata)

    return output

######################################################################
         
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
    
if __name__ == '__main__':
    test=Player('/home/juanpi/Projects/Eze/steeringbehaviors/steeringbehaviors/src/GameData/Player_demo.svg') 
    test.draw()
   

