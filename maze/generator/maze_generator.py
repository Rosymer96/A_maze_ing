#!/usr/bin/env python3
import random
from typing import Tuple, Optional
from maze.models import Maze
from maze.generator.recursive_backtracker import RecursiveBacktracker
from maze.utils import pattern_42
from maze.parser import ConfigError


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

        if seed is None:
            seed = random.randint(1, 999999)
        self.seed = seed
        self.rng = random.Random(self.seed)

        self.maze: Maze = Maze(self.width, self.height, self.entry, self.exit)

        my_map = [[cell.walls.value for cell in row] for row in self.maze.grid]
        my_visited = [[cell.visited for cell in row] for row in self.maze.grid]

        pattern_applied = pattern_42.apply_pattern_42(
            my_map, my_visited, self.width, self.height
        )

        if pattern_applied:
            # ── Protección: entry/exit no pueden caer dentro del patrón ──
            ex, ey = self.entry
            xx, xy = self.exit
            if my_visited[ey][ex]:
                raise ConfigError(
                    f"Entry {self.entry} falls inside the '42' pattern."
                )
            if my_visited[xy][xx]:
                raise ConfigError(
                    f"Exit {self.exit} falls inside the '42' pattern."
                )
            # ───────────────────────────────────────────────────────────
            from maze.utils.constants import Wall
            for y in range(self.height):
                for x in range(self.width):
                    if my_visited[y][x]:
                        self.maze.grid[y][x].visited = True
                        self.maze.grid[y][x].walls = Wall.ALL

    def generate(self) -> Maze:
        algorithm = RecursiveBacktracker(self.maze, self.rng)
        algorithm.run()
        return self.maze
