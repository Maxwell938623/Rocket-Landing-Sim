import pygame
import math

# Screen settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
COLUMNS, ROWS = WIDTH // CELL_SIZE - 10, HEIGHT // CELL_SIZE - 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Define constants (tuned PID parameters)
Kp_pos = 0
Kd_pos = 0
Kp_height = 2
Kd_alt = 180
Kp_vy = 8000
Kp_ang_vel = 0.8
Kp_angle = 5
MAX_THRUST_ANGLE = math.radians(70)
DAMPING = 0.98
MASS = 10
GRAVITY = 9.81

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Builder")
