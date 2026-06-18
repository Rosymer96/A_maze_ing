# Pixel grid for digit '4' (3 cols x 5 rows)
DIGIT_4 = [
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1]
]

# Pixel grid for digit '2' (3 cols x 5 rows)
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
    """Combine DIGIT_4 and DIGIT_2 with a gap column into a 5x7 pattern.

    Returns:
        A 5x7 binary grid where 1 marks a filled cell.
    """
    pattern = []
    for row_4, row_2 in zip(DIGIT_4, DIGIT_2):
        pattern.append(row_4 + [0] + row_2)
    return pattern


def apply_pattern_42(
    my_map: list[list[int]],
    my_visited: list[list[bool]],
    width: int,
    height: int
) -> bool:
    """Mark the '42' pattern cells as fully closed in the maze map.

    Cells belonging to the pattern are set to 15 (all walls closed)
    and marked as visited so the generator never carves through them.
    The pattern is centered in the maze grid.

    Args:
        my_map: 2D bitmask grid of the maze.
        my_visited: 2D visited flags grid.
        width: Number of columns in the maze.
        height: Number of rows in the maze.

    Returns:
        True if the pattern fits and was applied, False if the maze
        is too small to include it.
    """
    if width < PATTERN_WIDTH + 2 or height < PATTERN_HEIGHT + 2:
        return False

    pattern = get_pattern_42()

    start_x = (width - PATTERN_WIDTH) // 2
    start_y = (height - PATTERN_HEIGHT) // 2

    for dy, row in enumerate(pattern):
        for dx, val in enumerate(row):
            if val == 1:
                rx = start_x + dx
                ry = start_y + dy
                my_map[ry][rx] = 15
                my_visited[ry][rx] = True

    return True
