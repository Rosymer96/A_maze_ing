from maze.models.maze import Maze


class HexExporter:
    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze

    def export(self) -> str:
        """
        Traduce el estado actual del laberinto a una cadena de caracteres
        hexadecimales continua, siguiendo las especificaciones del subject.
        """
        hex_chars: list[str] = []

        # Recorremos la rejilla fila por fila (Y) y luego celda por celda (X)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.grid[y][x]

                # El valor de cell.walls ya es un entero gracias a IntFlag (ej. 15 para ALL)
                # La función nativa hex() de Python transforma un entero a hex (ej. 15 -> '0xf')
                # Usamos [2:] para quitar el prefijo '0x' y quedarnos solo con el carácter
                hex_char = hex(cell.walls.value)[2:]

                hex_chars.append(hex_char)

        # Unimos todos los caracteres en una sola línea continua sin espacios
        return "".join(hex_chars)
