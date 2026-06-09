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
    pattern = []
    for row_4, row_2 in zip(DIGIT_4, DIGIT_2):
        pattern.append(row_4 + [0] + row_2)
    return pattern


def apply_pattern_42(grid: Grid) -> bool:
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

                cell.north = True
                cell.east = True
                cell.south = True
                cell.west = True

    return True
