from vpython import *
import numpy as np

# recBox = box(pos=vector(0,0,0), size=vector(1,0.2,0.5), color=color.red)
# create an x,y,z coordinate system using arrows
x_axis = arrow(pos=vector(0,0,0), axis=vector(1,0,0), color=color.red, shaftwidth=0.02,length=5)
y_axis = arrow(pos=vector(0,0,0), axis=vector(0,1,0), color=color.green, shaftwidth=0.02,length=5)
z_axis = arrow(pos=vector(0,0,0), axis=vector(0,0,1), color=color.blue, shaftwidth=0.02,length=5)

myVecMag = 3.0
myVecAng = 120  # degrees
myVecXmag = myVecMag * np.cos(np.radians(myVecAng))
myVecYmag = myVecMag * np.sin(np.radians(myVecAng))
myVecZ = 0  # assuming a 2D vector in the XY plane

myVecX = arrow(pos=vector(0,0,0), axis=vector(1,0,0), color=vector(0,1,1), 
                   shaftwidth=0.02,length=myVecXmag)
myVecY = arrow(pos=vector(0,0,0), axis=vector(0,1,0), color=vector(1,0,1), 
                   shaftwidth=0.02,length=myVecYmag)

myVecRes = arrow(pos=vector(0,0,0), axis=vector(myVecXmag,myVecYmag,0), color=color.yellow, shaftwidth=0.02,length=myVecMag)

print("myVecXmag:", sign(myVecXmag))
print("myVecYmag:", sign(myVecYmag))
while True:
    # pass
    rate(30)
    myVecAng = myVecAng + 1
    myVecXmag = myVecMag * np.cos(np.radians(myVecAng))
    myVecYmag = myVecMag * np.sin(np.radians(myVecAng))
    myVecRes.axis = vector(myVecXmag, myVecYmag, 0)

    myVecX.pos = vector(0,myVecYmag,0)
    myVecX.axis = vector(myVecXmag, 0, 0)
    myVecY.pos = vector(myVecXmag, 0, 0)
    myVecY.axis = vector(0, myVecYmag, 0)

