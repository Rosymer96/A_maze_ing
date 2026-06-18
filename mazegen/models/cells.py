#!/usr/bin/env python3

from mazegen.utils.constants import Wall


class Cells:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        # Al inicio, todas las celdas empiezan completamente cerradas
        self.walls: Wall = Wall.ALL
        # Esta variable nos servirá para que el algoritmo sepa si ya pasó por aquí
        self.visited: bool = False

    def remove_wall(self, wall: Wall) -> None:
        """Rompe una pared específica usando operaciones de bits."""
        # El operador ~ invierte los bits.
        # Si ALL es 1111 y NORTH es 0001, ~NORTH se convierte en 1110.
        # Al hacer &= (AND), el bit de NORTH pasa a ser 0 (abierto).
        self.walls &= ~wall

    def has_wall(self, wall: Wall) -> bool:
        """Verifica si una pared específica está cerrada (devuelve True o False)."""
        # Hacemos una operación AND bit a bit (&).
        # Si el bit de la pared está en 1, el resultado será mayor que 0 (True).
        # Si el bit está en 0 (abierto), el resultado será 0 (False).
        return bool(self.walls & wall)
