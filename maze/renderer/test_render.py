from maze.models.grid_cell import Grid
from maze.renderer.ascii_render_v2 import AsciiRenderer
from maze.renderer.pattern_42 import apply_pattern_42


def build_test_maze() -> Grid:
    g = Grid(15, 11)

    #
    # ENTRADA
    #
    g.get_cell(0, 0).is_entry = True

    #
    # SALIDA
    #
    g.get_cell(14, 10).is_exit = True

    #
    # Camino manual para probar colores
    #
    path_coords = [
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
        (3, 2),
        (4, 2),
        (5, 2),
        (6, 2),
        (6, 3),
        (6, 4),
        (7, 4),
        (8, 4),
        (9, 4),
        (10, 4),
        (11, 4),
        (12, 4),
        (13, 4),
        (14, 4),
        (14, 5),
        (14, 6),
        (14, 7),
        (14, 8),
        (14, 9),
        (14, 10),
    ]

    for x, y in path_coords:
        g.get_cell(x, y).is_path = True

    #
    # Abrimos paredes siguiendo el path
    #
    for i in range(len(path_coords) - 1):
        x1, y1 = path_coords[i]
        x2, y2 = path_coords[i + 1]

        c1 = g.get_cell(x1, y1)
        c2 = g.get_cell(x2, y2)

        if x2 == x1 + 1:
            c1.east = False
            c2.west = False

        elif x2 == x1 - 1:
            c1.west = False
            c2.east = False

        elif y2 == y1 + 1:
            c1.south = False
            c2.north = False

        elif y2 == y1 - 1:
            c1.north = False
            c2.south = False

    #
    # Añadir el patrón 42
    #
    apply_pattern_42(g)

    return g

def main() -> None:
    maze = build_test_maze()

    renderer = AsciiRenderer()

    print(renderer.render(maze))


if __name__ == "__main__":
    main()
