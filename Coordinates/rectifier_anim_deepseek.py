import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Full Bridge Rectifier Animation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)

# Clock for controlling animation speed
clock = pygame.time.Clock()
FPS = 60

# Animation parameters
time = 0
animation_speed = 0.05

# Component positions
transformer_pos = (WIDTH // 4, HEIGHT // 2 - 50)
bridge_pos = (WIDTH // 2, HEIGHT // 2)
load_pos = (3 * WIDTH // 4, HEIGHT // 2)
capacitor_pos = (3 * WIDTH // 4, HEIGHT // 2 + 50)

# Diode states (True = conducting, False = blocking)
diode_states = [False, False, False, False]

# Current paths
current_paths = []

class Diode:
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.conducting = False
        
    def draw(self, screen):
        # Draw diode body
        diode_length = 30
        diode_width = 20
        
        # Calculate endpoints based on angle
        end_x = self.x + diode_length * math.cos(math.radians(self.angle))
        end_y = self.y + diode_length * math.sin(math.radians(self.angle))
        
        # Draw line
        color = RED if self.conducting else GRAY
        pygame.draw.line(screen, color, (self.x, self.y), (end_x, end_y), 3)
        
        # Draw triangle (arrowhead)
        triangle_size = 10
        angle_rad = math.radians(self.angle)
        
        # Points for the triangle
        p1 = (end_x, end_y)
        p2 = (end_x - triangle_size * math.cos(angle_rad) + triangle_size * 0.5 * math.cos(angle_rad + math.pi/2),
              end_y - triangle_size * math.sin(angle_rad) + triangle_size * 0.5 * math.sin(angle_rad + math.pi/2))
        p3 = (end_x - triangle_size * math.cos(angle_rad) + triangle_size * 0.5 * math.cos(angle_rad - math.pi/2),
              end_y - triangle_size * math.sin(angle_rad) + triangle_size * 0.5 * math.sin(angle_rad - math.pi/2))
        
        pygame.draw.polygon(screen, color, [p1, p2, p3])
        
        # Draw bar (cathode)
        bar_dist = 8
        bar_x = self.x + bar_dist * math.cos(angle_rad)
        bar_y = self.y + bar_dist * math.sin(angle_rad)
        
        bar_perp_x = bar_x + triangle_size * 0.7 * math.cos(angle_rad + math.pi/2)
        bar_perp_y = bar_y + triangle_size * 0.7 * math.sin(angle_rad + math.pi/2)
        bar_perp_x2 = bar_x + triangle_size * 0.7 * math.cos(angle_rad - math.pi/2)
        bar_perp_y2 = bar_y + triangle_size * 0.7 * math.sin(angle_rad - math.pi/2)
        
        pygame.draw.line(screen, color, (bar_perp_x, bar_perp_y), (bar_perp_x2, bar_perp_y2), 3)

class CurrentParticle:
    def __init__(self, path, speed=2):
        self.path = path
        self.speed = speed
        self.position = 0  # Position along the path (0 to 1)
        self.active = True
        
    def update(self):
        self.position += self.speed / 100
        if self.position >= 1:
            self.active = False
            
    def draw(self, screen):
        if not self.active:
            return
            
        # Find the point along the path
        idx = int(self.position * (len(self.path) - 1))
        idx = min(idx, len(self.path) - 1)
        pos = self.path[idx]
        
        pygame.draw.circle(screen, YELLOW, pos, 3)

# Create diodes
diodes = [
    Diode(bridge_pos[0] - 40, bridge_pos[1] - 40, 45),   # Top-left
    Diode(bridge_pos[0] + 40, bridge_pos[1] - 40, 135),  # Top-right
    Diode(bridge_pos[0] - 40, bridge_pos[1] + 40, -45),  # Bottom-left
    Diode(bridge_pos[0] + 40, bridge_pos[1] + 40, -135)  # Bottom-right
]

# Define paths for current flow
def create_path(start_pos, end_pos, curves=[]):
    path = []
    steps = 50
    
    for i in range(steps + 1):
        t = i / steps
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
        
        # Apply curves if any
        for curve in curves:
            if curve[0] <= t <= curve[1]:
                curve_t = (t - curve[0]) / (curve[1] - curve[0])
                curve_strength = curve[2] * math.sin(curve_t * math.pi)
                x += curve[3] * curve_strength
                y += curve[4] * curve_strength
                
        path.append((int(x), int(y)))
    
    return path

# Create paths for positive and negative half-cycles
positive_paths = [
    create_path((transformer_pos[0] + 50, transformer_pos[1] - 30), 
                (diodes[0].x, diodes[0].y)),
    create_path((diodes[0].x, diodes[0].y), 
                (load_pos[0] - 50, load_pos[1]), 
                [(0.5, 1.0, 20, 0, 1)]),
    create_path((load_pos[0] - 50, load_pos[1]), 
                (diodes[3].x, diodes[3].y),
                [(0.0, 0.5, 20, 0, -1)]),
    create_path((diodes[3].x, diodes[3].y), 
                (transformer_pos[0] + 50, transformer_pos[1] + 30))
]

negative_paths = [
    create_path((transformer_pos[0] + 50, transformer_pos[1] + 30), 
                (diodes[2].x, diodes[2].y)),
    create_path((diodes[2].x, diodes[2].y), 
                (load_pos[0] - 50, load_pos[1]), 
                [(0.5, 1.0, 20, 0, -1)]),
    create_path((load_pos[0] - 50, load_pos[1]), 
                (diodes[1].x, diodes[1].y),
                [(0.0, 0.5, 20, 0, 1)]),
    create_path((diodes[1].x, diodes[1].y), 
                (transformer_pos[0] + 50, transformer_pos[1] - 30))
]

# Main animation loop
running = True
particle_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Clear screen
    screen.fill(BLACK)
    
    # Update time
    time += animation_speed
    
    # Calculate AC voltage
    ac_voltage = math.sin(time)
    
    # Determine which diodes are conducting based on AC phase
    if ac_voltage > 0:  # Positive half-cycle
        diodes[0].conducting = True  # Top-left
        diodes[3].conducting = True  # Bottom-right
        diodes[1].conducting = False
        diodes[2].conducting = False
        active_paths = positive_paths
    else:  # Negative half-cycle
        diodes[1].conducting = True  # Top-right
        diodes[2].conducting = True  # Bottom-left
        diodes[0].conducting = False
        diodes[3].conducting = False
        active_paths = negative_paths
    
    # Draw transformer
    pygame.draw.rect(screen, BLUE, (transformer_pos[0] - 40, transformer_pos[1] - 60, 80, 120), 2)
    pygame.draw.line(screen, BLUE, (transformer_pos[0] - 40, transformer_pos[1] - 30), 
                    (transformer_pos[0] + 40, transformer_pos[1] - 30), 2)
    pygame.draw.line(screen, BLUE, (transformer_pos[0] - 40, transformer_pos[1] + 30), 
                    (transformer_pos[0] + 40, transformer_pos[1] + 30), 2)
    
    # Draw AC source symbol
    pygame.draw.circle(screen, GREEN, (transformer_pos[0] - 70, transformer_pos[1]), 15, 2)
    pygame.draw.line(screen, GREEN, (transformer_pos[0] - 85, transformer_pos[1]), 
                    (transformer_pos[0] - 55, transformer_pos[1]), 2)
    pygame.draw.line(screen, GREEN, (transformer_pos[0] - 75, transformer_pos[1] - 10), 
                    (transformer_pos[0] - 65, transformer_pos[1] + 10), 2)
    
    # Draw sine wave representing AC input
    wave_points = []
    for i in range(100):
        x = transformer_pos[0] - 100 + i * 2
        y = transformer_pos[1] + ac_voltage * 30 * math.sin(i * 0.2 - time * 2)
        wave_points.append((x, y))
    
    if len(wave_points) > 1:
        pygame.draw.lines(screen, GREEN, False, wave_points, 2)
    
    # Draw connections from transformer to bridge
    pygame.draw.line(screen, WHITE, (transformer_pos[0] + 40, transformer_pos[1] - 30), 
                    (bridge_pos[0] - 60, bridge_pos[1] - 40), 2)
    pygame.draw.line(screen, WHITE, (transformer_pos[0] + 40, transformer_pos[1] + 30), 
                    (bridge_pos[0] - 60, bridge_pos[1] + 40), 2)
    
    # Draw bridge rectifier
    pygame.draw.rect(screen, GRAY, (bridge_pos[0] - 50, bridge_pos[1] - 50, 100, 100), 2)
    
    # Draw diodes
    for diode in diodes:
        diode.draw(screen)
    
    # Draw load resistor
    pygame.draw.rect(screen, RED, (load_pos[0] - 50, load_pos[1] - 20, 100, 40), 2)
    pygame.draw.line(screen, RED, (load_pos[0] - 30, load_pos[1] - 20), 
                    (load_pos[0] - 30, load_pos[1] + 20), 2)
    pygame.draw.line(screen, RED, (load_pos[0] + 30, load_pos[1] - 20), 
                    (load_pos[0] + 30, load_pos[1] + 20), 2)
    
    # Draw capacitor
    pygame.draw.line(screen, BLUE, (capacitor_pos[0] - 30, capacitor_pos[1] - 15), 
                    (capacitor_pos[0] + 30, capacitor_pos[1] - 15), 2)
    pygame.draw.line(screen, BLUE, (capacitor_pos[0] - 30, capacitor_pos[1] + 15), 
                    (capacitor_pos[0] + 30, capacitor_pos[1] + 15), 2)
    pygame.draw.line(screen, BLUE, (capacitor_pos[0] - 20, capacitor_pos[1] - 15), 
                    (capacitor_pos[0] - 20, capacitor_pos[1] + 15), 2)
    pygame.draw.line(screen, BLUE, (capacitor_pos[0] + 20, capacitor_pos[1] - 15), 
                    (capacitor_pos[0] + 20, capacitor_pos[1] + 15), 2)
    
    # Draw connections
    pygame.draw.line(screen, WHITE, (bridge_pos[0] + 50, bridge_pos[1] - 40), 
                    (load_pos[0] - 50, load_pos[1]), 2)
    pygame.draw.line(screen, WHITE, (bridge_pos[0] + 50, bridge_pos[1] + 40), 
                    (capacitor_pos[0] - 50, capacitor_pos[1]), 2)
    pygame.draw.line(screen, WHITE, (load_pos[0] + 50, load_pos[1]), 
                    (capacitor_pos[0] + 50, capacitor_pos[1]), 2)
    pygame.draw.line(screen, WHITE, (capacitor_pos[0], capacitor_pos[1] + 30), 
                    (capacitor_pos[0], HEIGHT - 20), 2)
    pygame.draw.line(screen, WHITE, (bridge_pos[0] - 50, bridge_pos[1] + 40), 
                    (bridge_pos[0] - 80, bridge_pos[1] + 40), 2)
    pygame.draw.line(screen, WHITE, (bridge_pos[0] - 80, bridge_pos[1] + 40), 
                    (bridge_pos[0] - 80, HEIGHT - 20), 2)
    
    # Draw ground symbol
    pygame.draw.line(screen, GREEN, (bridge_pos[0] - 80, HEIGHT - 20), 
                    (bridge_pos[0] - 90, HEIGHT - 20), 2)
    pygame.draw.line(screen, GREEN, (bridge_pos[0] - 85, HEIGHT - 20), 
                    (bridge_pos[0] - 85, HEIGHT - 10), 2)
    pygame.draw.line(screen, GREEN, (bridge_pos[0] - 95, HEIGHT - 10), 
                    (bridge_pos[0] - 75, HEIGHT - 10), 2)
    pygame.draw.line(screen, GREEN, (bridge_pos[0] - 90, HEIGHT - 10), 
                    (bridge_pos[0] - 90, HEIGHT - 5), 2)
    pygame.draw.line(screen, GREEN, (bridge_pos[0] - 80, HEIGHT - 10), 
                    (bridge_pos[0] - 80, HEIGHT - 5), 2)
    
    # Draw DC output waveform
    dc_points = []
    for i in range(100):
        x = load_pos[0] + 60 + i * 2
        y = load_pos[1] - abs(ac_voltage) * 30 * math.sin(i * 0.2 - time * 2) - 10
        dc_points.append((x, y))
    
    if len(dc_points) > 1:
        pygame.draw.lines(screen, YELLOW, False, dc_points, 2)
    
    # Add current particles
    particle_timer += 1
    if particle_timer >= 5:  # Add a new particle every 5 frames
        particle_timer = 0
        for path in active_paths:
            current_paths.append(CurrentParticle(path))
    
    # Update and draw current particles
    for particle in current_paths[:]:
        particle.update()
        particle.draw(screen)
        if not particle.active:
            current_paths.remove(particle)
    
    # Draw labels
    font = pygame.font.SysFont(None, 24)
    text = font.render("AC Input", True, GREEN)
    screen.blit(text, (transformer_pos[0] - 120, transformer_pos[1] - 50))
    
    text = font.render("Bridge Rectifier", True, WHITE)
    screen.blit(text, (bridge_pos[0] - 60, bridge_pos[1] - 80))
    
    text = font.render("Load", True, RED)
    screen.blit(text, (load_pos[0] - 20, load_pos[1] - 50))
    
    text = font.render("Filter Capacitor", True, BLUE)
    screen.blit(text, (capacitor_pos[0] - 60, capacitor_pos[1] - 50))
    
    text = font.render("DC Output", True, YELLOW)
    screen.blit(text, (load_pos[0] + 60, load_pos[1] - 50))
    
    # Update display
    pygame.display.flip()
    
    # Control animation speed
    clock.tick(FPS)

pygame.quit()
sys.exit()