from dataclasses import dataclass
from maze.models.grid_cell import Grid


@dataclass
class RenderTheme:
    wall: str = "\033[93m█\033[0m"
    empty: str = " "

    path: str = "\033[96m█\033[0m"

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
    # 2 chars celda + 1 pared en X
    # 2 chars celda + 1 pared en Y  (×2 para compensar ratio char)
        width  = grid.width  * 4 + 1
        height = grid.height * 3 + 1  # ← cambia de *2+1 a *3+1

        canvas = [
            [self.theme.wall for _ in range(width)]
            for _ in range(height)
        ]

        for y in range(grid.height):
            for x in range(grid.width):
                cell = grid.get_cell(x, y)

                cx = x * 4 + 1
                cy = y * 3 + 1  # ← *3 en lugar de *2

                tile = self._cell_tile(cell)

                for dy in range(2):
                    for dx in range(3):
                        canvas[cy + dy][cx + dx] = tile

                # Norte
                if not cell.north:
                    for dx in range(3):
                        canvas[cy - 1][cx + dx] = self.theme.empty

                # Sur
                if not cell.south:
                    for dx in range(3):
                        canvas[cy + 2][cx + dx] = self.theme.empty

                # Oeste
                if not cell.west:
                    canvas[cy][cx - 1]     = self.theme.empty
                    canvas[cy + 1][cx - 1] = self.theme.empty

                # Este
                if not cell.east:
                    canvas[cy][cx + 3]     = self.theme.empty
                    canvas[cy + 1][cx + 3] = self.theme.empty

        return "\n".join("".join(row) for row in canvas)
