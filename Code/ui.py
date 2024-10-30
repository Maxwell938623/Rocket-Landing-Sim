import pygame
from settings import *
from rocket import load_rocket_shape, save_rocket_shape, clear_rocket_shape, is_connected, calculate_rocket_dimensions
from simulation import simulate_screen

def draw_button(x, y, width, height, text):
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(SCREEN, GRAY, button_rect)
    pygame.draw.rect(SCREEN, BLACK, button_rect, 2)
    text_surface = font.render(text, True, BLACK)
    SCREEN.blit(text_surface, (button_rect.x + 10, button_rect.y + 5))
    return button_rect

def handle_mouse_click(event, grid):
    if event.button == 1:  # Left mouse button
        mouse_x, mouse_y = event.pos
        if clear_button_rect.collidepoint(event.pos):
            grid = clear_rocket_shape()
        elif simulate_button_rect.collidepoint(event.pos):
            save_rocket_shape(grid)
            simulate_screen(grid)
        else:
            col = mouse_x // CELL_SIZE - 5
            row = mouse_y // CELL_SIZE - 5
            if 0 <= col < COLUMNS and 0 <= row < ROWS:
                # Toggle cell state if not the middle blue block
                if grid[row][col] == 1:
                    original_value = grid[row][col]
                    grid[row][col] = 0
                    if not is_connected(grid):
                        grid[row][col] = original_value
                elif grid[row][col] == 0:
                    original_value = grid[row][col]
                    grid[row][col] = 1
                    if not is_connected(grid):
                        grid[row][col] = original_value
    return grid
    

def draw_main_screen(grid):
    SCREEN.fill(WHITE)

    for row in range(ROWS):
        for col in range(COLUMNS):
            rect = pygame.Rect((col + 5) * CELL_SIZE, (row + 5) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == 1:
                pygame.draw.rect(SCREEN, RED, rect)
            elif grid[row][col] == 2:
                pygame.draw.rect(SCREEN, BLUE, rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)  # Draw cell border

    global clear_button_rect, simulate_button_rect
    clear_button_rect = draw_button(10, HEIGHT - 50, 170, 40, "Clear Rocket")
    simulate_button_rect = draw_button(220, HEIGHT - 50, 125, 40, "Simulate")

    _, _, rocket_width, rocket_height = calculate_rocket_dimensions(grid)
    rocket_width //= CELL_SIZE
    rocket_height //= CELL_SIZE
    font = pygame.font.Font(None, 36)
    dimension_text = f"Width: {rocket_width}, Height: {rocket_height}"
    dimension_surface = font.render(dimension_text, True, BLACK)
    SCREEN.blit(dimension_surface, (400, HEIGHT - 50))
