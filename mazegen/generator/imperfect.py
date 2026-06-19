import random
from typing import List, Tuple

from mazegen.models import Maze, Cells
from mazegen.utils import Wall, MOVES, OPPOSITE_WALL


class ImperfectMaze:
    """
    Removes additional internal walls from a perfect maze to introduce cycles.

    Preserves:
        - External walls
        - Cells belonging to the '42' pattern
        - Areas that would create a fully open 3x3 section
    """

    def __init__(
            self,
            maze: Maze,
            rng: random.Random,
            extra_wall_removal_chance: float = 0.12
    ) -> None:
        """
        Initialize an imperfect maze generator.

        Args:
            maze: Maze instance to modify.
            rng: Random generator used for reproducible changes.
            extra_wall_removal_chance: Probability of removing a
            candidate wall.
        """

        self.maze: Maze = maze
        self.rng = rng
        self.chance = extra_wall_removal_chance

    def _is_pattern_cell(self, cell: Cells) -> bool:
        """
        Check if a cell belongs to the protected 42 pattern.

        Args:
            cell: Cell to check.

        Returns:
            True if the cell is part of the pattern, otherwise False.
        """

        return cell.walls == Wall.ALL and cell.visited

    def _creates_3x3_open_area(
        self, x1: int,
        y1: int,
        x2: int,
        y2: int
    ) -> bool:
        """
        Check if removing a wall would create a fully open 3x3 area.

        Args:
            x1: X coordinate of first cell.
            y1: Y coordinate of first cell.
            x2: X coordinate of second cell.
            y2: Y coordinate of second cell.

        Returns:
            True if the change creates an open 3x3 area.
        """
        min_x = min(x1, x2)
        min_y = min(y1, y2)

        for top_x in range(min_x - 2, min_x + 1):
            for top_y in range(min_y - 2, min_y + 1):
                if self._window_would_be_fully_open(
                    top_x, top_y, x1, y1, x2, y2
                ):
                    return True
        return False

    def _window_would_be_fully_open(
        self,
        top_x: int,
        top_y: int,
        opened_x1: int,
        opened_y1: int,
        opened_x2: int,
        opened_y2: int
    ) -> bool:
        """
        Check if a 3x3 window would be fully connected.

        Args:
            top_x: Top-left X coordinate of the window.
            top_y: Top-left Y coordinate of the window.
            opened_x1: X coordinate of first modified cell.
            opened_y1: Y coordinate of first modified cell.
            opened_x2: X coordinate of second modified cell.
            opened_y2: Y coordinate of second modified cell.

        Returns:
            True if all internal walls would be open.
        """
        cells_in_window: List[Cells] = []
        for dy in range(3):
            for dx in range(3):
                cell = self.maze.get_cell(top_x + dx, top_y + dy)
                if cell is None:
                    return False  # ventana fuera del mapa, no aplica
                cells_in_window.append(cell)

        for cell in cells_in_window:
            for direction, (dx, dy) in MOVES.items():
                nx, ny = cell.x + dx, cell.y + dy
                neighbor = self.maze.get_cell(nx, ny)
                if neighbor is None or neighbor not in cells_in_window:
                    continue

                wall_open = not cell.has_wall(direction)

                # Simulate opening the selected wall.
                pair_a = (cell.x, cell.y) == (opened_x1, opened_y1) and \
                    (nx, ny) == (opened_x2, opened_y2)
                pair_b = (cell.x, cell.y) == (opened_x2, opened_y2) and \
                    (nx, ny) == (opened_x1, opened_y1)
                if pair_a or pair_b:
                    wall_open = True

                if not wall_open:
                    return False

        return True

    def apply(self) -> None:
        """
        Remove random internal walls while preserving maze constraints.
        """
        candidates: List[Tuple[Wall, Cells, Cells]] = []

        for row in self.maze.grid:
            for cell in row:
                if self._is_pattern_cell(cell):
                    continue

                for direction, (dx, dy) in MOVES.items():
                    neighbor = self.maze.get_cell(cell.x + dx, cell.y + dy)

                    if neighbor is None:
                        continue

                    if self._is_pattern_cell(neighbor):
                        continue

                    if not cell.has_wall(direction):
                        continue

                    candidates.append((direction, cell, neighbor))

        self.rng.shuffle(candidates)

        for direction, cell, neighbor in candidates:
            if self.rng.random() > self.chance:
                continue

            if self._creates_3x3_open_area(
                cell.x, cell.y, neighbor.x, neighbor.y
            ):
                continue

            cell.remove_wall(direction)
            neighbor.remove_wall(OPPOSITE_WALL[direction])
