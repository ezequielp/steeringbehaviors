import real2pix as rp
import numpy as np

camera=rp.transformation()
v=np.array([1,1])
print 'The input'
print v
# doesn't work, why?
vt=camera.transform(v)

# The intended functionanlity
#vt=np.round(np.dot(camera.T,np.transpose(np.concatenate((v,[1]))))[:2])
print 'The transformed input without setting the transform'
print vt

camera._set_transform(rotate=np.array([45]),scale=np.array([10,10]),
                      move=np.array([1,0]))
vt=camera.transform(v)

#print camera.T

#vt=np.round(np.dot(camera.T,np.transpose(np.concatenate((v,[1]))))[:2])
print 'The transformed input'
print 'Rotated 45deg, moved [1,0], Scaled x10'
print vt
                      
