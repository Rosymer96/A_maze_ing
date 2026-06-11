from dataclasses import dataclass
from maze.models.grid_cell import Grid


@dataclass
class RenderTheme:
    wall: str = "\033[94m█\033[0m"
    empty: str = " "

    path: str = "\033[35m█\033[0m"

    entry: str = "\033[92m█\033[0m"
    exit: str = "\033[91m█\033[0m"

    pattern42: str = "\033[37m█\033[0m"


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
    
    def _wall_tile(self, cell, neighbor) -> str:
        """Devuelve el tile para la pared entre cell y neighbor."""
        if (self.show_path 
            and cell.is_path 
            and neighbor is not None 
            and neighbor.is_path):
            return self.theme.path
        return self.theme.empty

    def render(self, grid: Grid) -> str:
        width = grid.width * 4 + 1
        height = grid.height * 3 + 1

        canvas = [
            [self.theme.wall for _ in range(width)]
            for _ in range(height)
        ]

        for y in range(grid.height):
            for x in range(grid.width):
                cell = grid.get_cell(x, y)

                cx = x * 4 + 1
                cy = y * 3 + 1

                tile = self._cell_tile(cell)

                for dy in range(2):
                    for dx in range(3):
                        canvas[cy + dy][cx + dx] = tile

                # Norte
                if not cell.north:
                    neighbor = grid.get_cell(x, y - 1) if y > 0 else None
                    wall = self._wall_tile(cell, neighbor)
                    for dx in range(3):
                        canvas[cy - 1][cx + dx] = wall

                # Sur
                if not cell.south:
                    neighbor = grid.get_cell(x, y + 1) if y < grid.height - 1 else None
                    wall = self._wall_tile(cell, neighbor)
                    for dx in range(3):
                        canvas[cy + 2][cx + dx] = wall

                # Oeste
                if not cell.west:
                    neighbor = grid.get_cell(x - 1, y) if x > 0 else None
                    wall = self._wall_tile(cell, neighbor)
                    canvas[cy][cx - 1]     = wall
                    canvas[cy + 1][cx - 1] = wall

                # Este
                if not cell.east:
                    neighbor = grid.get_cell(x + 1, y) if x < grid.width - 1 else None
                    wall = self._wall_tile(cell, neighbor)
                    canvas[cy][cx + 3]     = wall
                    canvas[cy + 1][cx + 3] = wall

        return "\n".join("".join(row) for row in canvas)
