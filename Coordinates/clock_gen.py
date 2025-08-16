from vpython import *
import math

# Create the scene
scene = canvas(width=800, height=800, background=color.white)

# Clock parameters
clock_radius = 5
clock_thickness = 0.2
hour_hand_length = 3
minute_hand_length = 4
second_hand_length = 4.5  # Slightly longer than minute hand
tick_length = 0.5
major_tick_thickness = 0.15
minor_tick_thickness = 0.05

# Time constants (in seconds)
SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 3600
SECONDS_IN_12HOURS = 43200

# Create clock face (disc)
clock_face = cylinder(
    pos=vector(0, 0, -clock_thickness/2),
    axis=vector(0, 0, clock_thickness),
    radius=clock_radius,
    color=color.white,
    opacity=1
)

# Create clock border
clock_border = ring(
    pos=vector(0, 0, 0),
    axis=vector(0, 0, 1),
    radius=clock_radius,
    thickness=0.2,
    color=color.black
)

# Create hour ticks and numbers
for i in range(12):
    angle = i * math.pi/6  # 360/12 = 30 degrees = pi/6 radians
    
    # Major tick marks (hours)
    start_pos = vector(clock_radius-tick_length, 0, 0)
    end_pos = vector(clock_radius, 0, 0)
    
    # Rotate positions
    start_pos = rotate(start_pos, angle=angle, axis=vector(0,0,1))
    end_pos = rotate(end_pos, angle=angle, axis=vector(0,0,1))
    
    # Create hour tick
    cylinder(
        pos=start_pos,
        axis=end_pos-start_pos,
        radius=major_tick_thickness,
        color=color.black
    )
    
    # Add hour numbers
    number_pos = rotate(vector(clock_radius-1.2, 0, 0), angle=angle, axis=vector(0,0,1))
    label(
        pos=number_pos,
        text=str((i + 3) % 12 if (i + 3) % 12 != 0 else 12),
        height=0.6,
        color=color.black,
        box=False
    )

# Create minute ticks
for i in range(60):
    if i % 5 != 0:  # Skip positions where hour ticks are
        angle = i * math.pi/30  # 360/60 = 6 degrees = pi/30 radians
        
        start_pos = vector(clock_radius-tick_length/2, 0, 0)
        end_pos = vector(clock_radius, 0, 0)
        
        # Rotate positions
        start_pos = rotate(start_pos, angle=angle, axis=vector(0,0,1))
        end_pos = rotate(end_pos, angle=angle, axis=vector(0,0,1))
        
        # Create minute tick
        cylinder(
            pos=start_pos,
            axis=end_pos-start_pos,
            radius=minor_tick_thickness,
            color=color.black
        )

# Create clock hands
hour_hand = arrow(
    pos=vector(0,0,0.1),
    axis=vector(hour_hand_length,0,0),
    shaftwidth=0.15,
    color=color.blue
)

minute_hand = arrow(
    pos=vector(0,0,0.2),
    axis=vector(minute_hand_length,0,0),
    shaftwidth=0.1,
    color=color.red
)

second_hand = arrow(
    pos=vector(0,0,0.3),
    axis=vector(second_hand_length,0,0),
    shaftwidth=0.05,
    color=color.green
)

# Center dot
center_dot = cylinder(
    pos=vector(0,0,0),
    axis=vector(0,0,0.5),
    radius=0.2,
    color=color.black
)

# Animation
elapsed_seconds = 0  # Track total elapsed seconds
dt = 1  # Time step (1 second)

while True:
    rate(1)  # Update every second
    
    elapsed_seconds += dt
    
    # Calculate angles based on elapsed time (negative for clockwise rotation)
    second_angle = -(elapsed_seconds % SECONDS_IN_MINUTE) * (2*pi/SECONDS_IN_MINUTE)
    minute_angle = -(elapsed_seconds % SECONDS_IN_HOUR) * (2*pi/SECONDS_IN_HOUR)
    hour_angle = -(elapsed_seconds % SECONDS_IN_12HOURS) * (2*pi/SECONDS_IN_12HOURS)
    
    # Rotate hands
    second_hand.axis = rotate(vector(second_hand_length,0,0), angle=second_angle, axis=vector(0,0,1))
    minute_hand.axis = rotate(vector(minute_hand_length,0,0), angle=minute_angle, axis=vector(0,0,1))
    hour_hand.axis = rotate(vector(hour_hand_length,0,0), angle=hour_angle, axis=vector(0,0,1))
