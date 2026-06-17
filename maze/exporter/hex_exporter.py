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

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.grid[y][x]

                hex_char = hex(cell.walls.value)[2:]

                hex_chars.append(hex_char)

        return "".join(hex_chars)
