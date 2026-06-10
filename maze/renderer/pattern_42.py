from maze.models.grid_cell import Grid

DIGIT_4 = [
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1]
]

DIGIT_2 = [
    [1, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1]
]

PATTERN_HEIGHT = 5
PATTERN_WIDTH = 7


def get_pattern_42() -> list[list[int]]:
    """Combine DIGIT_4 and DIGIT_2 with a gap column into a 5x7 pattern."""
    pattern = []
    for row_4, row_2 in zip(DIGIT_4, DIGIT_2):
        pattern.append(row_4 + [0] + row_2)
    return pattern


def apply_pattern_42(grid: Grid) -> bool:
    """
    Mark the 42 pattern cells as fully closed and also close
    the walls of their neighbours that face them, so no passage
    is rendered from either side.
    """
    if grid.width < PATTERN_WIDTH + 2 or grid.height < PATTERN_HEIGHT + 2:
        return False

    pattern = get_pattern_42()

    start_x = (grid.width - PATTERN_WIDTH) // 2
    start_y = (grid.height - PATTERN_HEIGHT) // 2

    for dy, row in enumerate(pattern):
        for dx, val in enumerate(row):
            if val == 1:
                cell = grid.get_cell(start_x + dx, start_y + dy)
                cell.is_pattern42 = True

                # Cerrar todas las paredes de la celda del patrón
                cell.north = True
                cell.east  = True
                cell.south = True
                cell.west  = True

                # Cerrar también la pared del vecino que apunta hacia aquí
                # para que el renderer no abra el pasillo desde ese lado
                nx, ny = start_x + dx, start_y + dy

                if ny > 0:
                    grid.get_cell(nx, ny - 1).south = True  # vecino norte
                if ny < grid.height - 1:
                    grid.get_cell(nx, ny + 1).north = True  # vecino sur
                if nx > 0:
                    grid.get_cell(nx - 1, ny).east  = True  # vecino oeste
                if nx < grid.width - 1:
                    grid.get_cell(nx + 1, ny).west  = True  # vecino este

    return True