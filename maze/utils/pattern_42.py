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


def apply_pattern_42(
    my_map: list[list[int]],
    my_visited: list[list[bool]],
    width: int,
    height: int
) -> bool:
    """
    Marca las celdas del patrón 42 en my_map con valor 15
    (todas las paredes cerradas) y las marca como visitadas
    para que el generador no las toque.

    Returns:
        True si el patrón cabe, False si el laberinto es demasiado pequeño.
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
                my_map[ry][rx] = 15     # todas las paredes cerradas
                my_visited[ry][rx] = True   # el generador no la visita

    return True
