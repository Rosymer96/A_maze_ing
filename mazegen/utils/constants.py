from enum import IntFlag
from typing import Dict, Tuple


class Wall(IntFlag):
    """Bitmask enumeration representing the four walls of a maze cell.

    Each value corresponds to a single bit:
        NORTH = 0001, EAST = 0010, SOUTH = 0100, WEST = 1000.
    """

    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL = 15


# Maps each wall direction to its (dx, dy) movement vector
MOVES: Dict[Wall, Tuple[int, int]] = {
    Wall.NORTH: (0, -1),
    Wall.EAST: (1, 0),
    Wall.SOUTH: (0, 1),
    Wall.WEST: (-1, 0)
}

# Maps each wall direction to the opposite wall in the neighboring cell
OPPOSITE_WALL: Dict[Wall, Wall] = {
    Wall.NORTH: Wall.SOUTH,
    Wall.EAST: Wall.WEST,
    Wall.SOUTH: Wall.NORTH,
    Wall.WEST: Wall.EAST
}
