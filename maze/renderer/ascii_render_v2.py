from dataclasses import dataclass
from maze.models.grid_cell import Grid


@dataclass
class RenderTheme:
    wall: str = "\033[93m█\033[0m"
    empty: str = " "

    path: str = "\033[96m·\033[0m"

    entry: str = "\033[92m█\033[0m"
    exit: str = "\033[91m█\033[0m"

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
        width = grid.width * 3 + 1
        height = grid.height * 2 + 1

        canvas = [
            [self.theme.wall for _ in range(width)]
            for _ in range(height)
        ]

        for y in range(grid.height):
            for x in range(grid.width):
                cell = grid.get_cell(x, y)

                cx = x * 3 + 1
                cy = y * 2 + 1

                tile = self._cell_tile(cell)  # calcular una sola vez

                # Interior: aplicar el tile a los 2 chars
                canvas[cy][cx]     = tile
                canvas[cy][cx + 1] = tile

                # Norte/Sur
                if not cell.north:
                    canvas[cy - 1][cx]     = self.theme.empty
                    canvas[cy - 1][cx + 1] = self.theme.empty

                if not cell.south:
                    canvas[cy + 1][cx]     = self.theme.empty
                    canvas[cy + 1][cx + 1] = self.theme.empty

                # Oeste / Este
                if not cell.west:
                    canvas[cy][cx - 1] = self.theme.empty

                if not cell.east:
                    canvas[cy][cx + 2] = self.theme.empty

        return "\n".join("".join(row) for row in canvas)