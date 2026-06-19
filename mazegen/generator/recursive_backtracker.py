import random
from typing import List, Tuple

from mazegen.models import Maze, Cells
from mazegen.utils import Wall, MOVES, OPPOSITE_WALL


class RecursiveBacktracker:
    """
    Generates a perfect maze using the recursive backtracking algorithm.
    """

    def __init__(self, maze: Maze, rng: random.Random) -> None:
        """
        Initialize the maze generator.

        Args:
            maze: Maze instance to modify.
            rng: Random generator used for cell selection.
        """
        self.maze: Maze = maze
        self.rng = rng

    def _get_unvisited_neighbors(
        self,
        cells: Cells
    ) -> List[Tuple[Wall, Cells]]:
        """
        Get adjacent cells that have not been visited yet.

        Args:
            cells: Current cell to inspect.

        Returns:
            List of possible directions and unvisited neighbor cells.
        """
        neighbors: List[Tuple[Wall, Cells]] = []

        # Check all possible movement directions.
        for direction, (dx, dy) in MOVES.items():
            next_x = cells.x + dx
            next_y = cells.y + dy

            neighbor = self.maze.get_cell(next_x, next_y)
            if neighbor and not neighbor.visited:
                neighbors.append((direction, neighbor))

        return neighbors

    def run(self) -> None:
        """
        Generate the maze using recursive backtracking.

        Starts from the entry cell, removes walls between visited cells,
        and backtracks when no unvisited neighbors are available.
        """
        start_x, start_y = self.maze.entry
        current_cell = self.maze.grid[start_y][start_x]

        current_cell.visited = True
        stack: List[Cells] = []

        while True:
            unvisited = self._get_unvisited_neighbors(current_cell)

            if unvisited:
                # Choose a random unvisited neighbor.
                direction, next_cell = self.rng.choice(unvisited)

                stack.append(current_cell)

                # Remove walls between current and next cell.
                current_cell.remove_wall(direction)
                next_cell.remove_wall(OPPOSITE_WALL[direction])

                next_cell.visited = True
                current_cell = next_cell

            elif stack:
                # Backtrack to the previous cell.
                current_cell = stack.pop()

            else:
                # Generation finished.
                break
