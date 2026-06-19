#!/usr/bin/env python3
import random
from typing import Tuple, Optional

from mazegen.models import Maze
from mazegen.generator.recursive_backtracker import RecursiveBacktracker
from mazegen.utils import pattern_42
from mazegen.generator.imperfect import ImperfectMaze
from mazegen.exporter import HexExporter
from mazegen.solver import MazeSolver
from mazegen.utils import Wall


class MazeGeneratorError(Exception):
    """Error raised by MazeGenerator."""
    pass


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool,
        seed: Optional[int] = None,
        my_map: Optional[list[list[int]]] = None
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.perfect: bool = perfect

        if seed is None:
            seed = random.randint(1, 999999)
        self.seed = seed
        self.rng = random.Random(self.seed)
        self._solution: Optional[tuple[list[tuple[int, int]], str]] = None

        self.maze: Maze = Maze(self.width, self.height, self.entry, self.exit)
        self._apply_pattern_42_to_maze()

    def _apply_pattern_42_to_maze(self) -> None:
        """
        Apply the '42' pattern to the maze grid.

        Raises:
            MazeGeneratorError: If the entry or exit falls inside
            the '42' pattern.
        """

        my_map = [[cell.walls.value for cell in row] for row in self.maze.grid]
        my_visited = [[cell.visited for cell in row] for row in self.maze.grid]

        pattern_applied = pattern_42.apply_pattern_42(
            my_map, my_visited, self.width, self.height
        )

        if not pattern_applied:
            print("\033[1;91m"
                  "\nThe maze is too small to include the '42' pattern.\n"
                  "\033[0m")

        ex, ey = self.entry
        xx, xy = self.exit
        if my_visited[ey][ex]:
            raise MazeGeneratorError(
                f"Entry {self.entry} falls inside the '42' pattern."
            )
        if my_visited[xy][xx]:
            raise MazeGeneratorError(
                f"Exit {self.exit} falls inside the '42' pattern."
            )

        for y in range(self.height):
            for x in range(self.width):
                if my_visited[y][x]:
                    self.maze.grid[y][x].visited = True
                    self.maze.grid[y][x].walls = Wall.ALL

    def generate(self) -> Maze:
        """
        Generate the maze.

        Returns:
            The generated maze.
        """

        self._solution = None

        algorithm = RecursiveBacktracker(self.maze, self.rng)
        algorithm.run()

        if not self.perfect:
            imperfect = ImperfectMaze(self.maze, self.rng)
            imperfect.apply()

        return self.maze

    def solve(self) -> tuple[list[tuple[int, int]], str]:
        """
        Resolve the maze using BFS.

        Returns:
            A tuple containing the solution path and its string representation.
        Raises:
            MazeGeneratorError: If generate() has not been called.
        """

        if self._solution is not None:
            return self._solution

        self.my_map = [
            [int(cell.walls.value) for cell in row]
            for row in self.maze.grid
        ]
        solver = MazeSolver()
        path_coords, path_str = solver.solve(
            self.my_map,
            self.entry,
            self.exit
            )

        if not path_coords:
            raise MazeGeneratorError("No solution found.")

        self._solution = (path_coords, path_str)
        return self._solution

    def export(self, output_file: str) -> None:
        """
        Resolve and save the maze in hexa format.

        Args:
            output_file: The path to the output file.
        """

        _, path_str = self.solve()

        exporter = HexExporter(self.maze)
        exporter.write(
            output_file=output_file,
            entry=self.entry,
            exit=self.exit,
            path_str=path_str
        )
