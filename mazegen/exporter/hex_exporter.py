from mazegen.models import Maze


class HexExporter:
    """Exports a maze to hexadecimal format as specified by the subject."""

    def __init__(self, maze: Maze) -> None:
        """Initialize the exporter with a generated maze.

        Args:
            maze: The maze object to export.
        """
        self.maze: Maze = maze

    def export(self) -> str:
        """
        Translate the maze grid to a hexadecimal string representation.

        Each cell is encoded as a single hex digit where each bit represents
        a wall: bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West.
        A set bit means the wall is closed.

        Returns:
            A string with one hex row per line, uppercase, no separators.
        """
        hex_chars: list[str] = []

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.grid[y][x]

                # Convert wall bitmask to uppercase hex digit (e.g. 15 -> 'F')
                hex_char = hex(cell.walls.value)[2:].upper()
                hex_chars.append(hex_char)
            hex_chars.append("\n")
        return "".join(hex_chars)

    def write(
        self,
        output_file: str,
        entry: tuple[int, int],
        exit: tuple[int, int],
        path_str: str
    ) -> None:
        """Write the full maze output file as required by the subject.

        The file contains the hex grid, followed by a blank line, then
        the entry coordinates, exit coordinates, and shortest path.

        Args:
            output_file: Path to the output file.
            entry: Entry coordinates as (x, y).
            exit: Exit coordinates as (x, y).
            path_str: Shortest path from entry to exit using N, E, S, W.
        """

        content = self.export()
        content += f"\n{entry[0]},{entry[1]}\n"     # entry
        content += f"{exit[0]},{exit[1]}\n"       # exit
        content += f"{path_str}"                   # path

        with open(output_file, "w") as f:
            f.write(content)
