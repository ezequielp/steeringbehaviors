'''
Created on 16/11/2009

@author: Ezequiel N. Pozzo
Edited by JuanPi Carbajal
'''
import numpy as np
import real2pix as rp

class View(object):
'''
An abstract class for Viewers
'''
    def __init__(self, Model):
        pass
    
    def update(self):
        pass
        

class View2D(View):
'''
A class for Viewers of 2D Models
'''
    def __init__(self,Model):
        # Base class initialization 
        View.__init__(self, Model)
       
        # JPi: How do we define private variables and methods?
        self._sprites=np.array([])
        self._project=rp.Transformation()
    
    def update(self):
        View.update(self)
        # Here sprites are updated. How? Idea: apply the transformation
        # self._project.transformation(Model.actors) or something like that.
        pass
            
class PygameViewer(View2D):
'''
A class rendering the actors of the Model into a Pygame window
'''        
    # JPi: Here is Ezequiels Magic!
    
