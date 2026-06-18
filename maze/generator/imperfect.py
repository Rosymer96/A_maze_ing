import random
from typing import List, Tuple
from maze.models import Maze, Cells
from maze.utils import Wall, MOVES, OPPOSITE_WALL


class ImperfectMaze:
    """
    Rompe paredes internas adicionales sobre un laberinto perfecto ya
    generado, para introducir ciclos (PERFECT=False).

    No toca:
      - paredes externas (el borde del maze)
      - celdas marcadas como parte del patrón '42' (cell.visited tras
        MazeGenerator las deja en True con walls=ALL)
      - nada que produzca un área abierta de 3x3 o mayor
    """

    def __init__(
            self,
            maze: Maze,
            rng: random.Random,
            extra_wall_removal_chance: float = 0.12
    ) -> None:
        self.maze: Maze = maze
        self.rng = rng
        self.chance = extra_wall_removal_chance

    def _is_pattern_cell(self, cell: Cells) -> bool:
        """Una celda del patrón 42 tiene todas las paredes y nunca se toca."""
        return cell.walls == Wall.ALL and cell.visited

    def _creates_3x3_open_area(
        self, x1: int,
        y1: int,
        x2: int,
        y2: int
    ) -> bool:
        """
        Comprueba si abrir la pared entre (x1,y1) y (x2,y2) generaría
        un bloque de 3x3 celdas totalmente interconectadas.

        Estrategia simple: para cada ventana 3x3 que contenga ambas
        celdas, contamos cuántas de las 12 paredes internas de esa
        ventana estarían abiertas DESPUÉS del cambio. Si las 12 lo
        estarían, es una zona 3x3 completamente abierta.
        """

        # Las ventanas 3x3 candidatas son las que tienen su esquina
        # superior-izquierda en un rango que cubra ambas celdas.
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
        """Comprueba una ventana 3x3 concreta con esquina en (top_x, top_y)."""
        cells_in_window: List[Cells] = []
        for dy in range(3):
            for dx in range(3):
                cell = self.maze.get_cell(top_x + dx, top_y + dy)
                if cell is None:
                    return False  # ventana fuera del mapa, no aplica
                cells_in_window.append(cell)

        # Para cada pareja de celdas horizontalmente o verticalmente
        # adyacentes DENTRO de la ventana, comprobamos si la pared
        # entre ellas estaría abierta (considerando el cambio hipotético).
        for cell in cells_in_window:
            for direction, (dx, dy) in MOVES.items():
                nx, ny = cell.x + dx, cell.y + dy
                neighbor = self.maze.get_cell(nx, ny)
                if neighbor is None or neighbor not in cells_in_window:
                    continue  # vecino fuera de la ventana, no cuenta

                wall_open = not cell.has_wall(direction)

                # Si esta es justo la pared que estamos planteando abrir,
                # la tratamos como abierta para esta simulación.
                pair_a = (cell.x, cell.y) == (opened_x1, opened_y1) and \
                    (nx, ny) == (opened_x2, opened_y2)
                pair_b = (cell.x, cell.y) == (opened_x2, opened_y2) and \
                    (nx, ny) == (opened_x1, opened_y1)
                if pair_a or pair_b:
                    wall_open = True

                if not wall_open:
                    return False  # hay al menos una pared cerrada, no es 3x3

        return True

    def apply(self) -> None:
        """Recorre el maze y rompe paredes internas extra al azar."""
        candidates: List[Tuple[Wall, Cells, Cells]] = []

        for row in self.maze.grid:
            for cell in row:
                if self._is_pattern_cell(cell):
                    continue

                for direction, (dx, dy) in MOVES.items():
                    neighbor = self.maze.get_cell(cell.x + dx, cell.y + dy)

                    # Sin vecino = sería pared exterior, nunca se toca
                    if neighbor is None:
                        continue

                    if self._is_pattern_cell(neighbor):
                        continue

                    # Solo nos interesan paredes que AÚN están cerradas
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
