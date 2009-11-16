'''
Created on 16/11/2009

@author: Ezequiel N. Pozzo
Edited by JuanPi Carbajal
'''
from __future__ import division
import numpy as np

class View(object):
    '''
    An abstract class for Viewers
    '''
    def __init__(self, Model):
        self._model=Model
        
    
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
    
    def set_transform(self,move=np.array([0,0]), rotate=np.array([0]),scale=np.array([1,1])):
        # Works only in 2D for the moment                                 
                    
        # Rotation
        R = rotv(np.array([0,0,1]),rotate[0])
        # Scale
        S = np.diag(np.concatenate([scale,[1]]))
        
        # Translation
        A = zeros([3,3])
        for i in xrange(0,2):
            A[i,-1]=move[i]*scale[i]

        self.T=dot(R,S)+A  
                  
class PygameViewer(View2D):
'''
A class rendering the actors of the Model into a Pygame window
'''        
    # JPi: Here is Ezequiels Magic!
    
