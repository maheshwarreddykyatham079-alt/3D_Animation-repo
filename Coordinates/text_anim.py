from vpython import *
import numpy as np

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


# Set up camera view
scene.camera.pos = vector(0,0,15)
scene.camera.axis = -scene.camera.pos

# Text parameters
myText = "R"
text_height = 0.1      # Overall height of the text
text_depth = 0.3     # Thickness/depth of the text

# Create 3D text
t1 = text(text="R", pos=vector(0, -text_height/2, 0), color=color.red, 
          height=text_height, depth=text_height/3, align='center')
slope = -3

while True:
    pass
    #   for text_height in np.linspace(0.1, 2, 100):
    #     rate(10)
    #     t1.height = text_height
    #     t1.depth = text_height/3  # Adjust width based on height
    #     t1.pos = vector(text_height*slope/2, -text_height/2, text_height)
# t2 = text(text="A", pos=vector(0, -text_height/2, 0), color=color.red, height=text_height, depth=text_depth, align='center')  
# slope = -2
# for text_height in np.linspace(0.1, 2, 100):
#         rate(50)
#         t2.height = text_height
#         t2.pos = vector(text_height*slope/2, -text_height/2, text_height)

# t3 = text(text="H", pos=vector(0, -text_height/2, 0), color=color.red, height=text_height, depth=text_depth, align='center')
# slope = -1
# for text_height in np.linspace(0.1, 2, 100):
#         rate(50)
#         t3.height = text_height
#         t3.pos = vector(text_height*slope/2, -text_height/2, text_height)

# t4 = text(text="U", pos=vector(0, -text_height/2, 0), color=color.red, height=text_height, depth=text_depth, align='center')
# slope = 0
# for text_height in np.linspace(0.1, 2, 100):
#         rate(50)
#         t4.height = text_height
#         t4.pos = vector(text_height*slope/2, -text_height/2, text_height)

# t5 = text(text="L", pos=vector(0, -text_height/2, 0), color=color.red, height=text_height, depth=text_depth, align='center')
# slope = 1
# for text_height in np.linspace(0.1, 2, 100):
#         rate(50)
#         t5.height = text_height
#         t5.pos = vector(text_height*slope/2, -text_height/2, text_height)





