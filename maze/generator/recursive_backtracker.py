import random
from typing import List, Tuple
from maze.models.maze import Maze
from maze.models.cells import Cells
from maze.utils.constants import Wall, MOVES, OPPOSITE_WALL


class RecursiveBacktracker:
    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze

    def _get_unvisited_neighbors(self, cells: Cells) -> List[Tuple[Wall, Cells]]:
        """Busca todas las celdas vecinas que aún no han sido visitadas."""
        neighbors: List[Tuple[Wall, Cells]] = []

        for direction, (dx, dy) in MOVES.items():
            next_x = cells.x + dx
            next_y = cells.y + dy

            neighbor = self.maze.get_cell(next_x, next_y)
            if neighbor and not neighbor.visited:
                neighbors.append((direction, neighbor))

        return neighbors

    def run(self) -> None:
        """Ejecuta el algoritmo para esculpir el laberinto perfecto."""
        start_x, start_y = self.maze.entry
        current_cell = self.maze.grid[start_y][start_x]

        current_cell.visited = True
        stack: List[Cells] = []

        while True:
            unvisited = self._get_unvisited_neighbors(current_cell)

            if unvisited:
                direction, next_cell = random.choice(unvisited)

                stack.append(current_cell)

                current_cell.remove_wall(direction)
                next_cell.remove_wall(OPPOSITE_WALL[direction])

                next_cell.visited = True
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()
            else:
                break
