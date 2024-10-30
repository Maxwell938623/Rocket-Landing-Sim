import json
import sys
from settings import *
from collections import deque

# Load rocket shape from a file
def load_rocket_shape():
    try:
        with open("rocket_shape.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

# Save rocket shape to a file
def save_rocket_shape(grid):
    with open("rocket_shape.json", "w") as file:
        json.dump(grid, file)

# Clear the JSON file
def clear_rocket_shape():
    global grid
    grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
    grid[ROWS // 2][COLUMNS // 2] = 2
    save_rocket_shape(grid)
    return grid

# Check if all red cells are connected to the blue cell
def is_connected(grid):
    visited = [[False for _ in range(COLUMNS)] for _ in range(ROWS)]
    middle_row, middle_col = ROWS // 2, COLUMNS // 2
    queue = deque([(middle_row, middle_col)])
    visited[middle_row][middle_col] = True

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLUMNS and not visited[nr][nc] and grid[nr][nc] != 0:
                visited[nr][nc] = True
                queue.append((nr, nc))

    for row in range(ROWS):
        for col in range(COLUMNS):
            if grid[row][col] == 1 and not visited[row][col]:
                return False
    return True

# Calculate the center of mass of the rocket
def calculate_center_of_mass(grid):
    total_mass = 0
    sum_x = 0
    sum_y = 0
    for row in range(ROWS):
        for col in range(COLUMNS):
            if grid[row][col] == 1 or grid[row][col] == 2:
                total_mass += 1
                sum_x += col
                sum_y += row
    if total_mass == 0:
        return None  # No cells
    return sum_x / total_mass, sum_y / total_mass

# Calculate the dimensions of the rocket
def calculate_rocket_dimensions(grid):
    min_row, max_row = ROWS, 0
    min_col, max_col = COLUMNS, 0
    for row in range(ROWS):
        for col in range(COLUMNS):
            if grid[row][col] == 1 or grid[row][col] == 2:
                min_row = min(min_row, row)
                max_row = max(max_row, row)
                min_col = min(min_col, col)
                max_col = max(max_col, col)
    if min_row == ROWS or min_col == COLUMNS:
        return 0, 0, 0, 0  # No rocket parts found
    width = (max_col - min_col + 1) * CELL_SIZE
    height = (max_row - min_row + 1) * CELL_SIZE
    return min_col, min_row, width, height

# Calculate rotational inertia of the rocket
def calculate_mass_rotational_inertia(grid, center_of_mass):
    com_x, com_y = center_of_mass
    inertia = 0
    mass = 0
    for row in range(ROWS):
        for col in range(COLUMNS):
            if grid[row][col] == 1 or grid[row][col] == 2:
                dx = col - com_x
                dy = row - com_y
                inertia += dx ** 2 + dy ** 2
                mass += 1
    return mass, inertia

