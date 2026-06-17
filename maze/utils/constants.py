from enum import IntFlag
from typing import Dict, Tuple


class Wall(IntFlag):
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL = 15


MOVES: Dict[Wall, Tuple[int, int]] = {
    Wall.NORTH: (0, -1),
    Wall.EAST: (1, 0),
    Wall.SOUTH: (0, 1),
    Wall.WEST: (-1, 0)
}

OPPOSITE_WALL: Dict[Wall, Wall] = {
    Wall.NORTH: Wall.SOUTH,
    Wall.EAST: Wall.WEST,
    Wall.SOUTH: Wall.NORTH,
    Wall.WEST: Wall.EAST
}
