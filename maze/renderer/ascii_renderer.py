from maze.models.grid_cell import Grid, Cell


class AsciiRenderer:
    def render(self, grid: Grid) -> str:
        output = ""

        # TOP BORDER
        output += "+" + "---+" * grid.width + "\n"

        for y in range(grid.height):
            # walls west + cells
            line = "|"

            for x in range(grid.width):
                cell = grid.cells[y][x]

                line += "   "  # cell space

                if cell.east:
                    line += "|"
                else:
                    line += " "

            output += line + "\n"

            # north/south walls
            line = "+"

            for x in range(grid.width):
                cell = grid.cells[y][x]

                if cell.south:
                    line += "---+"
                else:
                    line += "   +"

            output += line + "\n"

        return output
