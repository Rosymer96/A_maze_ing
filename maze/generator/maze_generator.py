#!/usr/bin/env python3
import random
from typing import Tuple, Optional
from maze.models.maze import Maze
from maze.generator.recursive_backtracker import RecursiveBacktracker
import maze.pattern_42 as pattern_42


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        seed: Optional[int] = None
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit

        if seed is not None:
            random.seed(seed)

        self.maze: Maze = Maze(self.width, self.height, self.entry, self.exit)

        my_map = [[cell.walls.value for cell in row] for row in self.maze.grid]
        my_visited = [[cell.visited for cell in row] for row in self.maze.grid]

        pattern_applied = pattern_42.apply_pattern_42(
            my_map, my_visited, self.width, self.height
        )

        if pattern_applied:
            from maze.utils.constants import Wall
            for y in range(self.height):
                for x in range(self.width):
                    if my_visited[y][x]:
                        self.maze.grid[y][x].visited = True
                        self.maze.grid[y][x].walls = Wall.ALL

    def generate(self) -> Maze:
        algorithm = RecursiveBacktracker(self.maze)
        algorithm.run()
        return self.maze
