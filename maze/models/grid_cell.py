from dataclasses import dataclass
from typing import List


@dataclass
class Cell:
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
    visited: bool = False
    is_entry: bool = False
    is_exit: bool = False
    is_path: bool = False
    is_pattern42: bool = False


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells: List[List[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]
