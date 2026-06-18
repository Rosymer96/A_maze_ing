from typing import List, Tuple, Optional
from maze.models.cells import Cells


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int]
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit

        # Creamos la rejilla de celdas usando una lista de comprensión
        #  (list comprehension)
        # Es una matriz donde accedemos primero por filas (y) y luego por
        #  columnas (x): self.grid[y][x]
        self.grid: List[List[Cells]] = [
            [Cells(x, y) for x in range(width)] for y in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Optional[Cells]:
        """Devuelve la celda en las coordenadas (x, y) si está dentro de los
          límites."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
