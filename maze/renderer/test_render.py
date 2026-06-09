from maze.models.grid_cell import Grid
from maze.renderer.ascii_renderer import AsciiRenderer


def build_test_maze():
    g = Grid(4, 3)

    # abrir algunos caminos manualmente

    # conectar (0,0) -> (1,0)
    g.cells[0][0].east = False
    g.cells[1][0].west = False

    # conectar (1,0) -> (1,1)
    g.cells[1][0].south = False
    g.cells[1][1].north = False

    # conectar (1,1) -> (2,1)
    g.cells[1][1].east = False
    g.cells[2][1].west = False
    return g


def main() -> None:
    maze = build_test_maze()
    renderer = AsciiRenderer()
    output = renderer.render(maze)
    print(output)


if __name__ == "__main__":
    main()
