import random
from typing import List, Tuple
from maze.models import Maze, Cells
from maze.utils import Wall, MOVES, OPPOSITE_WALL


class RecursiveBacktracker:
    def __init__(self, maze: Maze, rng: random.Random) -> None:
        self.maze: Maze = maze
        self.rng = rng

    def _get_unvisited_neighbors(
        self,
        cells: Cells
    ) -> List[Tuple[Wall, Cells]]:
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

    # El bucle continuará hasta que hayamos visitado todo y la pila vuelva
        while True:
            unvisited = self._get_unvisited_neighbors(current_cell)

            if unvisited:
                # Paso A: Elegir un vecino al azar
                direction, next_cell = self.rng.choice(unvisited)

                stack.append(current_cell)

    # Paso C: ¡Romper las paredes en ambas celdas para mantener la coherencia!
                current_cell.remove_wall(direction)
                next_cell.remove_wall(OPPOSITE_WALL[direction])

                next_cell.visited = True
                current_cell = next_cell
    # Si llegamos a un callejón sin salida, hacemos BACKTRACK:
    # Sacamos la última celda de la pila y regresamos a ella
            elif stack:
                current_cell = stack.pop()
# Si no hay vecinas libres y la pila está vacía... ¡Laberinto terminado!
            else:
                break
