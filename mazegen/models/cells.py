from mazegen.utils.constants import Wall


class Cells:
    """Represents a single cell in the maze grid."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize a cell at the given coordinates.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.
        """

        self.x: int = x
        self.y: int = y
        # All walls start closed
        self.walls: Wall = Wall.ALL
        # Tracks whether the generation algorithm has visited this cell
        self.visited: bool = False

    def remove_wall(self, wall: Wall) -> None:
        """Open a specific wall using bitwise operations.

        Args:
            wall: The wall direction to open.
        """
        # ~wall inverts the bits (e.g. NORTH=0001 → ~NORTH=1110)
        # &= clears the target bit, marking the wall as open
        self.walls &= ~wall

    def has_wall(self, wall: Wall) -> bool:
        """Check whether a specific wall is closed.

        Args:
            wall: The wall direction to check.

        Returns:
            True if the wall is closed, False if open.
        """
        # Bitwise AND: returns non-zero (True) if the wall bit is set

        return bool(self.walls & wall)
