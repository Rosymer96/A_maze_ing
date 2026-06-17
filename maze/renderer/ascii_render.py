from dataclasses import dataclass


@dataclass
class RenderTheme:
    wall: str = "\033[94m█\033[0m"
    empty: str = " "

    path: str = "\033[35m█\033[0m"

    entry: str = "\033[92m█\033[0m"
    exit: str = "\033[91m█\033[0m"

    pattern42: str = "\033[97m█\033[0m"

    @staticmethod
    def classic() -> "RenderTheme":
        return RenderTheme()

    @staticmethod
    def neon() -> "RenderTheme":
        return RenderTheme(
            wall="\033[32m█\033[0m",
            path="\033[94m█\033[0m",
            entry="\033[91m█\033[0m",
            exit="\033[93m█\033[0m",
            pattern42="\033[95m█\033[0m",
        )


class AsciiRenderer:

    def __init__(
        self,
        theme: RenderTheme | None = None,
        show_path: bool = False,
        show_42: bool = True,
        path: list[tuple[int, int]] | None = None,
    ):
        self.theme = theme or RenderTheme()
        self.show_path = show_path
        self.show_42 = show_42
        self._path_set: set[tuple[int, int]] = set(path) if path else set()

    def set_theme(self, theme: RenderTheme) -> None:
        """Cambia el tema en caliente."""
        self.theme = theme

    def set_path(self, path: list[tuple[int, int]]) -> None:
        """Actualiza el path de solución, al llamar al solver"""
        self._path_set = set(path)

    def _cell_tile(
        self,
        bits: int,
        x: int,
        y: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> str:
        if (x, y) == entry:
            return self.theme.entry

        if (x, y) == exit_:
            return self.theme.exit

        if self.show_path and (x, y) in self._path_set:
            return self.theme.path

        if self.show_42 and bits == 15:
            return self.theme.pattern42

        return self.theme.empty

    def _wall_tile(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """Pared entre dos celdas — path color si ambas son path."""
        if (self.show_path
                and (x1, y1) in self._path_set
                and (x2, y2) in self._path_set):
            return self.theme.path
        return self.theme.empty

    def render(
        self,
        my_map: list[list[int]],
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> str:
        height = len(my_map)
        width = len(my_map[0])

        canvas_w = width * 3 + 1
        canvas_h = height * 2 + 1

        canvas = [
            [self.theme.wall for _ in range(canvas_w)]
            for _ in range(canvas_h)
        ]

        for y in range(height):
            for x in range(width):
                bits = my_map[y][x]

                cx = x * 3 + 1
                cy = y * 2 + 1

                tile = self._cell_tile(bits, x, y, entry, exit_)

                # Interior 1×1
                canvas[cy][cx] = tile
                canvas[cy][cx + 1] = tile

                # Norte — bit 0
                if not (bits & 1):
                    wall = self._wall_tile(x, y, x, y - 1)
                    canvas[cy - 1][cx] = wall
                    canvas[cy - 1][cx + 1] = wall

                # Este — bit 1
                if not (bits & 2):
                    wall = self._wall_tile(x, y, x + 1, y)
                    canvas[cy][cx + 2] = wall

                # Sur — bit 2
                if not (bits & 4):
                    wall = self._wall_tile(x, y, x, y + 1)
                    canvas[cy + 1][cx] = wall

                # Oeste — bit 3
                if not (bits & 8):
                    wall = self._wall_tile(x, y, x - 1, y)
                    canvas[cy][cx - 1] = wall

        return "\n".join("".join(row) for row in canvas) + "\n"


'''
    def render(
        self,
        my_map: list[list[int]],
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> str:
        height = len(my_map)
        width = len(my_map[0])

        canvas_w = width * 3 + 1
        canvas_h = height * 3 + 1

        canvas = [
            [self.theme.wall for _ in range(canvas_w)]
            for _ in range(canvas_h)
        ]

        for y in range(height):
            for x in range(width):
                bits = my_map[y][x]

                cx = x * 3 + 1
                cy = y * 3 + 1

                tile = self._cell_tile(bits, x, y, entry, exit_)

                for dy in range(2):
                    for dx in range(2):
                        canvas[cy + dy][cx + dx] = tile

                # Norte — bit 0
                if not (bits & 1):
                    wall = self._wall_tile(x, y, x, y - 1)
                    for dx in range(2):
                        canvas[cy - 1][cx + dx] = wall

                # Este — bit 1
                if not (bits & 2):
                    wall = self._wall_tile(x, y, x + 1, y)
                    canvas[cy][cx + 2] = wall
                    canvas[cy + 1][cx + 2] = wall

                # Sur — bit 2
                if not (bits & 4):
                    wall = self._wall_tile(x, y, x, y + 1)
                    for dx in range(2):
                        canvas[cy + 2][cx + dx] = wall

                # Oeste — bit 3
                if not (bits & 8):
                    wall = self._wall_tile(x, y, x - 1, y)
                    canvas[cy][cx - 1] = wall
                    canvas[cy + 1][cx - 1] = wall

        return "\n".join("".join(row) for row in canvas) + "\n"
'''
