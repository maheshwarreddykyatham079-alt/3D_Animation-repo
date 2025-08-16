from vpython import *
import numpy as np

# recBox = box(pos=vector(0,0,0), size=vector(1,0.2,0.5), color=color.red)
# create an x,y,z coordinate system using arrows
Px_axis = arrow(pos=vector(0,0,0), axis=vector(1,0,0), color=color.red, shaftwidth=0.02,length=5)
Py_axis = arrow(pos=vector(0,0,0), axis=vector(0,1,0), color=color.green, shaftwidth=0.02,length=5)
Pz_axis = arrow(pos=vector(0,0,0), axis=vector(0,0,1), color=color.blue, shaftwidth=0.02,length=5)
Nx_axis = arrow(pos=vector(0,0,0), axis=vector(-1,0,0), color=color.red, shaftwidth=0.02,length=5)
Ny_axis = arrow(pos=vector(0,0,0), axis=vector(0,-1,0), color=color.green, shaftwidth=0.02,length=5)
Nz_axis = arrow(pos=vector(0,0,0), axis=vector(0 ,0,-1), color=color.blue, shaftwidth=0.02,length=5)

myVecMag = 3.0
myVecAng = 0  # degrees
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

xy=1
yz=0
zy=0

while True:
    # pass
    rate(150)
    myVecAng = myVecAng + 1
    myVecXmag = myVecMag * np.cos(np.radians(myVecAng))
    myVecYmag = myVecMag * np.sin(np.radians(myVecAng))
    
    if xy == 1:
        myVecRes.axis = vector(myVecXmag, myVecYmag, 0)
        if myVecAng >= 360:
            myVecRes.axis = vector(myVecXmag,0, myVecYmag)
            if myVecAng >= 810:
                myVecRes.axis = vector(0, -myVecXmag, myVecYmag)
                if myVecAng >= 1170:
                    myVecRes.axis = vector(-myVecXmag, 0, myVecYmag)
                    if myVecAng >= 1260:
                        myVecAng = 0





    # myVecX.pos = vector(0,myVecYmag,0)
    # myVecX.axis = vector(myVecXmag, 0, 0)
    # myVecY.pos = vector(myVecXmag, 0, 0)
    # myVecY.axis = vector(0, myVecYmag, 0)

