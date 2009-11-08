'''
Created on 08/11/2009

@author: Ezequiel N. Pozzo
'''
from numpy import array
import platform

zero_tuple=(0.0,0.0)
screen_size=(640,480)
assert not platform.system()=='Java', "Jython not implemented yet"

if not globals().has_key('client'):
    client="standalone"
    
    


