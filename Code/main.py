import pygame
import sys
from settings import *
from rocket import load_rocket_shape, save_rocket_shape, clear_rocket_shape, is_connected, calculate_rocket_dimensions
from ui import draw_button, draw_main_screen, handle_mouse_click
from simulation import simulate_screen

def main():
    global grid
    grid = load_rocket_shape()

    # Set the middle cell to be an unremovable blue block
    middle_row, middle_col = ROWS // 2, COLUMNS // 2
    grid[middle_row][middle_col] = 2

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_rocket_shape(grid)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                grid = handle_mouse_click(event, grid)

        # Drawing the grid and buttons
        draw_main_screen(grid)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
