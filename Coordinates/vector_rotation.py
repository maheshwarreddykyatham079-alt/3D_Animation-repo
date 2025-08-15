from vpython import *
import numpy as np

# Create canvas
scene = canvas(width=800, height=600)

# Vector parameters
vector_length = 3  # Length of the resultant vector

# Create vectors
# Main rotating vector (resultant)
resultant = arrow(pos=vector(0,0,0), 
                 axis=vector(vector_length,0,0), 
                 color=color.yellow,
                 shaftwidth=0.1)

# Component vectors
vector_x = arrow(pos=vector(0,0,0), 
                axis=vector(vector_length,0,0), 
                color=color.red,
                shaftwidth=0.1)   # X component

vector_y = arrow(pos=vector(0,0,0), 
                axis=vector(0,0,0), 
                color=color.blue,
                shaftwidth=0.1)  # Y component

# Animation parameters
angle = 0
rotation_speed = 0.05  # radians per frame

while True:
    rate(30)  # 30 frames per second
    
    # Update angle
    angle += rotation_speed
    
    # Calculate new positions for resultant vector
    x = vector_length * cos(angle)
    y = vector_length * sin(angle)
    
    # Calculate component lengths
    x_length = abs(x)  # Length of x component
    y_length = abs(y)  # Length of y component
    
    # Update resultant vector
    resultant.axis = vector(x, y, 0)
    
    # Update component vectors
    vector_x.axis = vector(x, 0, 0)  # X component
    vector_y.pos = vector(x, 0, 0)    # Y component starts where X component ends
    vector_y.axis = vector(0, y, 0)   # Y component
    
    # Display the lengths (optional)
    scene.caption = f"Resultant length: {vector_length:.1f}\nX component: {x_length:.1f}\nY component: {y_length:.1f}"
    
    # Optional: Add labels or text to show angles and magnitudes
    # scene.caption = f"Angle: {degrees(angle):.1f}°"
