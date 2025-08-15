from vpython import *
import numpy as np
myVecMag = 3.0
myVecAng = 120  # degrees
myVecXmag = myVecMag * np.cos(np.radians(myVecAng))
myVecYmag = myVecMag * np.sin(np.radians(myVecAng))
myVecZ = 0  # assuming a 2D vector in the XY plane

myVecX = arrow(pos=vector(0,myVecYmag,0), axis=vector(1,0,0), color=vector(0,1,1), 
                   shaftwidth=0.02,length=myVecXmag)  # Points diagonally

while True:
    rate(10)
    
    myVecAng = myVecAng + 1
    myVecXmag = myVecMag * np.cos(myVecAng/180 * np.pi)
    myVecX.length = myVecXmag
    myVecYmag = myVecMag * np.sin(myVecAng/180 * np.pi)
    
