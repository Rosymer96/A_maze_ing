from typing import List, Tuple, Optional
from mazegen.models.cells import Cells


class Maze:
    """Represents the maze grid and its metadata."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int]
    ) -> None:
        """Initialize the maze with the given dimensions and entry/exit points.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
            entry: Entry coordinates as (x, y).
            exit: Exit coordinates as (x, y).
        """
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit

        # 2D grid of cells accessed as grid[y][x]
        self.grid: List[List[Cells]] = [
            [Cells(x, y) for x in range(width)] for y in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Optional[Cells]:
        """Return the cell at coordinates (x, y) if within bounds.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            The cell at (x, y), or None if out of bounds.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
