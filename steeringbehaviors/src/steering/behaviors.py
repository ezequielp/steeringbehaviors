'''
Created on 08/11/2009

@author: Ezequiel N. Pozzo
'''
from numpy import sqrt, dot

class steerForSeek(object):
    def __init__(self, agent):
        self._agent=agent
        
    def get_steering_force(self, target):
        out=(target.position-self._agent.position)
        return out*0.1/sqrt(dot(out,out))