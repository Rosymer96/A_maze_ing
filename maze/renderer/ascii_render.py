from dataclasses import dataclass


@dataclass
class RenderTheme:
    """Visual theme used by the ASCII renderer."""

    wall: str = "\033[94m█\033[0m"
    empty: str = " "

    path: str = "\033[35m█\033[0m"

    entry: str = "\033[92m█\033[0m"
    exit: str = "\033[91m█\033[0m"

    pattern42: str = "\033[93m█\033[0m"

    @staticmethod
    def classic() -> "RenderTheme":
        """Return the default color theme."""
        return RenderTheme()

    @staticmethod
    def neon() -> "RenderTheme":
        """Return an alternative neon-style color theme."""
        return RenderTheme(
            wall="\033[95m█\033[0m",
            path="\033[93m█\033[0m",
            entry="\033[92m█\033[0m",
            exit="\033[91m█\033[0m",
            pattern42="\033[97m█\033[0m",
        )

    def neon_sec() -> "RenderTheme":
        """Return an alternative neon-style color theme."""
        return RenderTheme(
            wall="\033[93m█\033[0m",
            path="\033[94m█\033[0m",
            entry="\033[92m█\033[0m",
            exit="\033[91m█\033[0m",
            pattern42="\033[91m█\033[0m",
        )


class AsciiRenderer:
    """
    Render a maze in the terminal using ASCII/ANSI characters.

    Supports:
        - Colored walls
        - Solution path visualization
        - Entry and exit highlighting
        - 42 pattern highlighting
    """
    def __init__(
        self,
        theme: RenderTheme | None = None,
        show_path: bool = False,
        show_42: bool = True,
        path: list[tuple[int, int]] | None = None,
    ):
        """
        Initialize the renderer.

        Args:
            theme: Rendering theme.
            show_path: Whether to display the solution path.
            show_42: Whether to highlight 42 pattern cells.
            path: Optional solution path.
        """
        self.theme = theme or RenderTheme()
        self.show_path = show_path
        self.show_42 = show_42
        self._path_set: set[tuple[int, int]] = set(path) if path else set()

    def set_theme(self, theme: RenderTheme) -> None:
        """Change the rendering theme."""
        self.theme = theme

    def set_path(self, path: list[tuple[int, int]]) -> None:
        """Update the solution path."""
        self._path_set = set(path)

    def _cell_tile(
        self,
        bits: int,
        x: int,
        y: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> str:
        """
        Determine the visual representation of a maze cell.
        """
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
        """
        Return the wall representation between two adjacent cells.

        If both cells belong to the solution path, the wall is rendered
        using the path color to create a continuous highlighted route.
        """
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
        """
        Render the maze as a colored ASCII string.

        Args:
            my_map: Maze encoded as wall bit masks.
            entry: Entry cell coordinates.
            exit_: Exit cell coordinates.

        Returns:
            Rendered maze string.
        """
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

                # Draw cell interior
                canvas[cy][cx] = tile
                canvas[cy][cx + 1] = tile

                # North wall — bit 0
                if not (bits & 1):
                    wall = self._wall_tile(x, y, x, y - 1)
                    canvas[cy - 1][cx] = wall
                    canvas[cy - 1][cx + 1] = wall

                # East wall — bit 1
                if not (bits & 2):
                    wall = self._wall_tile(x, y, x + 1, y)
                    canvas[cy][cx + 2] = wall

                # South wall — bit 2
                if not (bits & 4):
                    wall = self._wall_tile(x, y, x, y + 1)
                    canvas[cy + 1][cx] = wall

                # West wall — bit 3
                if not (bits & 8):
                    wall = self._wall_tile(x, y, x - 1, y)
                    canvas[cy][cx - 1] = wall

        return "\n".join("".join(row) for row in canvas) + "\n"
