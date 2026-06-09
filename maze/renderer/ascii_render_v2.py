from dataclasses import dataclass
from maze.models.grid_cell import Grid


@dataclass
class RenderTheme:
    wall: str = "\033[93m█\033[0m"
    empty: str = " "

    path: str = "\033[96m·\033[0m"

    entry: str = "\033[92mE\033[0m"
    exit: str = "\033[91mX\033[0m"

    pattern42: str = "\033[95m█\033[0m"


class AsciiRenderer:

    def __init__(
        self,
        theme: RenderTheme | None = None,
        show_path: bool = True,
        show_42: bool = True,
    ):
        self.theme = theme or RenderTheme()
        self.show_path = show_path
        self.show_42 = show_42

    def _cell_tile(self, cell) -> str:

        if cell.is_entry:
            return self.theme.entry

        if cell.is_exit:
            return self.theme.exit

        if self.show_path and cell.is_path:
            return self.theme.path

        if self.show_42 and cell.is_pattern42:
            return self.theme.pattern42

        return self.theme.empty

    def render(self, grid: Grid) -> str:
    # Cada celda ocupa 2 chars de ancho × 1 char de alto
    # Canvas: width = cols*2+1 (paredes), height = rows*2+1
        width  = grid.width  * 3 + 1   # 2 chars celda + 1 pared
        height = grid.height * 2 + 1   # 1 char celda + 1 pared

        canvas = [
            [self.theme.wall for _ in range(width)]
            for _ in range(height)
        ]

        for y in range(grid.height):
            for x in range(grid.width):
                cell = grid.get_cell(x, y)

                cx = x * 3 + 1   # columna izquierda del interior (2 chars)
                cy = y * 2 + 1   # fila del interior (1 char)

                # Interior de la celda: 2 chars de ancho, 1 de alto
                canvas[cy][cx]     = self.theme.empty
                canvas[cy][cx + 1] = self.theme.empty

                # Tile en el primer char del centro
                canvas[cy][cx] = self._cell_tile(cell)

                # Norte / Sur: abrir 2 chars de ancho
                if not cell.north:
                    canvas[cy - 1][cx]     = self.theme.empty
                    canvas[cy - 1][cx + 1] = self.theme.empty

                if not cell.south:
                    canvas[cy + 1][cx]     = self.theme.empty
                    canvas[cy + 1][cx + 1] = self.theme.empty

                # Oeste / Este: 1 char de alto (ya es 1)
                if not cell.west:
                    canvas[cy][cx - 1] = self.theme.empty

                if not cell.east:
                    canvas[cy][cx + 2] = self.theme.empty   # justo después de los 2 chars

        return "\n".join("".join(row) for row in canvas)
