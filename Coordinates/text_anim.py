from vpython import *

# Create the scene
scene = canvas(width=800, height=800, background=color.black)

# Coordinate system parameters
def create_axes(axis_length):
    # Create coordinate axes using cylinders instead of arrows
    # X axis
    x_axis = cylinder(pos=vector(-axis_length,0,0), axis=vector(2*axis_length,0,0), 
                     radius=0.01, color=color.red)
    # Y axis
    y_axis = cylinder(pos=vector(0,-axis_length,0), axis=vector(0,2*axis_length,0), 
                     radius=0.01, color=color.green)
    # Z axis
    z_axis = cylinder(pos=vector(0,0,-axis_length), axis=vector(0,0,2*axis_length), 
                     radius=0.01, color=color.blue)
    return x_axis, y_axis, z_axis

axis_length = 10
create_axes(axis_length)

# Add axis labels
label(pos=vector(axis_length+1,0,0), text="X", color=color.red)
label(pos=vector(0,axis_length+1,0), text="Y", color=color.green)
label(pos=vector(0,0,axis_length+1), text="Z", color=color.blue)

# Set up camera view
scene.camera.pos = vector(15,15,15)
scene.camera.axis = -scene.camera.pos

# Your existing text animation setup
pz = -1
myText = "R"
t = text(text=myText, pos=vector(0, 0, pz), height=2, color=color.red, align='center')

while True:
    rate(30)
    pz= pz + 0.01
    if pz < 1:
        t.pos = vector(0, 0, pz)

