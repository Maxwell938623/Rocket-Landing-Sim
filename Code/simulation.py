import pygame
import sys
import math
from settings import *
from rocket import *
from ui import *

def draw_button(x, y, width, height, text):
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(SCREEN, GRAY, button_rect)
    pygame.draw.rect(SCREEN, BLACK, button_rect, 2)
    text_surface = font.render(text, True, BLACK)
    SCREEN.blit(text_surface, (button_rect.x + 10, button_rect.y + 5))
    return button_rect

# Rocket landing simulation screen
def rocket_landing_screen(grid):
    HEIGHT = 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    SCREEN.fill(WHITE)
    min_col, min_row, rocket_width, rocket_height = calculate_rocket_dimensions(grid)
    center_of_mass = calculate_center_of_mass(grid)
    rocket_cells = [(row, col) for row in range(ROWS) for col in range(COLUMNS) if grid[row][col] == 1 or grid[row][col] == 2]

    velocity_y = 2
    velocity_x = 0 
    rocket_y_offset = 50
    rocket_x_offset = WIDTH // 2 - rocket_width // 2
    ground_level = HEIGHT - 80

    body_angle = math.radians(100)
    angular_velocity = 0
    angular_acceleration = 0.0

    thrust_angle = 0
    previous_error = 0
    previous_altitude_error = 0
    
    factor_slow = 1
    factor_upright = 0.1
    factor_toggle = 0

    reached_zero = False
    
    mass, rotational_inertia = calculate_mass_rotational_inertia(grid, center_of_mass)

    landing = True
    while landing:
        SCREEN.fill(WHITE)

        if (velocity_y <= 0):
            velocity_y = 0
            landing = False
        elif (velocity_y < 50):
            factor_slow -= 0.05
            factor_slow = max(factor_slow, -0.05)
        else:
            factor_slow += 0.05
            factor_slow = min(factor_slow, 1)
            
        if (abs(math.degrees(body_angle) <= 50)):
            factor_upright += 0.05
            factor_upright = min(factor_upright, 1)
            
        position_error = rocket_x_offset - WIDTH // 2
        angular_velocity_error = -angular_velocity
        angle_error = -body_angle
        
        thrust_adjustment = (
            Kp_pos * position_error +
            Kd_pos * (position_error - previous_error) +
            Kp_ang_vel * angular_velocity_error +
            Kp_angle * angle_error
        )
        
        previous_error = position_error

        if ((rocket_y_offset + rocket_height - (ground_level - 50)) > 0):
            factor_toggle += 0.02
            factor_toggle = min(factor_toggle, 1)
        else:
            factor_toggle = 0

        THRUST_FORCE = (
            max(Kp_height * (rocket_y_offset + rocket_height - (ground_level - 30)), 0) +
            max(Kd_alt * pow(max(rocket_y_offset - rocket_height - previous_altitude_error, 0), 2.5) * factor_toggle, 0) + 
            max(Kp_vy * (1/(min(velocity_y,30)+1)) * factor_slow * factor_upright, -8) +
            MASS * GRAVITY
        ) * (1+(rotational_inertia/100)*(1/(velocity_y+1)))

        THRUST_FORCE = max(min(THRUST_FORCE, 2000), 0)

        previous_altitude_error = rocket_y_offset - rocket_height
        
        if (reached_zero):
            THRUST_FORCE = 0

        thrust_angle = max(-MAX_THRUST_ANGLE, min(MAX_THRUST_ANGLE, thrust_adjustment))

        torque = THRUST_FORCE * math.sin(thrust_angle) * (rocket_height / 2)
        angular_acceleration = torque / (rotational_inertia * 10)
        angular_velocity += angular_acceleration * 0.01
        body_angle += angular_velocity * 0.01

        total_thrust_angle = thrust_angle - body_angle

        thrust_x = THRUST_FORCE * math.sin(total_thrust_angle)
        thrust_y = THRUST_FORCE * math.cos(total_thrust_angle)

        acceleration_x = thrust_x / MASS
        acceleration_y = GRAVITY - (thrust_y / MASS)

        velocity_x += acceleration_x *0.05
        velocity_y += acceleration_y *0.05

        rocket_x_offset += velocity_x * 0.05
        rocket_y_offset += velocity_y * 0.05

        rect = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)

        for row, col in rocket_cells:
            translated_x = rocket_x_offset + (col - min_col) * CELL_SIZE
            translated_y = rocket_y_offset + (row - min_row) * CELL_SIZE

            rotated_x = (translated_x - WIDTH // 2) * math.cos(body_angle) - (translated_y - rocket_y_offset) * math.sin(body_angle) + WIDTH // 2
            rotated_y = (translated_x - WIDTH // 2) * math.sin(body_angle) + (translated_y - rocket_y_offset) * math.cos(body_angle) + rocket_y_offset

            rect.fill(RED if grid[row][col] == 1 else BLUE)

            rotated_rect = pygame.transform.rotate(rect, math.degrees(-body_angle))
            rect_position = rotated_rect.get_rect(center=(rotated_x, rotated_y))

            SCREEN.blit(rotated_rect, rect_position)

            half_size = CELL_SIZE // 2
            corners = [
                (-half_size, -half_size),
                (half_size, -half_size),
                (half_size, half_size),
                (-half_size, half_size)
            ]

            rotated_corners = []
            for x, y in corners:
                rotated_x = x * math.cos(body_angle) - y * math.sin(body_angle) + rect_position.centerx
                rotated_y = x * math.sin(body_angle) + y * math.cos(body_angle) + rect_position.centery
                rotated_corners.append((rotated_x, rotated_y))

            pygame.draw.polygon(SCREEN, BLACK, rotated_corners, 2)

            if grid[row][col] == 2:  # Assuming blue is the base
                rocket_bottom_x = rotated_x
                rocket_bottom_y = rotated_y + CELL_SIZE / 2

        ground_rect = pygame.Rect(0, ground_level, WIDTH, 10)
        pygame.draw.rect(SCREEN, BLACK, ground_rect)

        if rocket_bottom_x is not None and rocket_bottom_y is not None:
            flame_length = 20* math.sqrt(THRUST_FORCE) // 10

            flame_end_x = rocket_bottom_x + flame_length * math.sin(total_thrust_angle)
            flame_end_y = rocket_bottom_y + flame_length * math.cos(total_thrust_angle)

            pygame.draw.line(SCREEN, ORANGE, (rocket_bottom_x, rocket_bottom_y), (flame_end_x, flame_end_y), 5)

        pygame.display.flip()
        pygame.time.delay(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

    return_button_rect = draw_button(WIDTH // 2 - 100, HEIGHT - 50, 200, 35, "Return to Main")
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and return_button_rect.collidepoint(event.pos):
                    HEIGHT = 600
                    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
                    waiting = False
                    
def simulate_screen(grid):
    SCREEN.fill(WHITE)

    min_col, min_row, rocket_width, rocket_height = calculate_rocket_dimensions(grid)
    if rocket_width == 0 or rocket_height == 0:
        zoom_factor = 1
        offset_x = 0
        offset_y = 0
    else:
        zoom_factor = min(WIDTH / rocket_width, HEIGHT / rocket_height) * 0.5
        offset_x = (WIDTH - rocket_width * zoom_factor) / 2 - min_col * CELL_SIZE * zoom_factor
        offset_y = (HEIGHT - rocket_height * zoom_factor) / 2 - min_row * CELL_SIZE * zoom_factor

    for row in range(ROWS):
        for col in range(COLUMNS):
            if grid[row][col] == 1:
                rect = pygame.Rect(col * CELL_SIZE * zoom_factor + offset_x, row * CELL_SIZE * zoom_factor + offset_y, CELL_SIZE * (zoom_factor+0.1), CELL_SIZE * (zoom_factor+0.1))
                pygame.draw.rect(SCREEN, RED, rect)
                pygame.draw.rect(SCREEN, BLACK, rect, 2) 
            elif grid[row][col] == 2:
                rect = pygame.Rect(col * CELL_SIZE * zoom_factor + offset_x, row * CELL_SIZE * zoom_factor + offset_y, CELL_SIZE * (zoom_factor+0.1), CELL_SIZE * (zoom_factor+0.1))
                pygame.draw.rect(SCREEN, BLUE, rect)
                pygame.draw.rect(SCREEN, BLACK, rect, 2) 

    center_of_mass = calculate_center_of_mass(grid)
    if center_of_mass:
        com_x, com_y = center_of_mass
        com_x = (com_x+0.5) * CELL_SIZE * zoom_factor + offset_x
        com_y = (com_y+0.5) * CELL_SIZE * zoom_factor + offset_y
        pygame.draw.circle(SCREEN, GREEN, (int(com_x), int(com_y)), 5)

    continue_button_rect = draw_button(WIDTH // 2 + 10, HEIGHT - 80, 130, 35, "Continue")
    back_button_rect = draw_button(WIDTH // 2 - 90, HEIGHT - 80, 80, 35, "Back")
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if continue_button_rect.collidepoint(event.pos):
                        waiting = False
                        rocket_landing_screen(grid) 
                    elif back_button_rect.collidepoint(event.pos):
                        return
