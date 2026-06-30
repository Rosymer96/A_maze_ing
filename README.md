*This project has been created as part of the 42 curriculum by rosvela, jreyes-s. Version final*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator and visualizer written in Python 3. The program reads a configuration file, generates a maze using the Recursive Backtracker algorithm, solves it using BFS, and displays the result in the terminal with ANSI color rendering. The maze is also exported to a file using a hexadecimal wall representation as specified by the 42 subject.

Key features:
- Perfect and imperfect maze generation (configurable via `PERFECT` flag)
- Reproducible generation via seed
- Visual "42" pattern embedded in the maze
- Interactive terminal UI with color themes and solution path toggle
- Hexadecimal output file with entry, exit, and shortest path
- Reusable maze generation module (`mazegen`) installable via pip

---

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
make install
```

This automatically creates a `.venv` virtual environment, installs dependencies, and builds the package.

### Run

```bash
make run config.txt
```

Or manually:

```bash
python3 a_maze_ing.py config.txt
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
make lint-strict  # optional, stricter mypy checks
```

### Clean

```bash
make clean
```

### Build the reusable package

```bash
make build
```

This generates `mazegen-1.0.0-py3-none-any.whl` at the root of the repository.

---

## Configuration File

The program reads a plain text configuration file with one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored.

### Format

```
# Example config.txt
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `WIDTH` | int | ✅ | Number of columns in the maze |
| `HEIGHT` | int | ✅ | Number of rows in the maze |
| `ENTRY` | x,y | ✅ | Entry coordinates (must be inside bounds) |
| `EXIT` | x,y | ✅ | Exit coordinates (must be inside bounds, different from entry) |
| `OUTPUT_FILE` | str | ✅ | Path to the output hex file |
| `PERFECT` | bool | ✅ | `True` for a perfect maze, `False` for imperfect (with loops) |
| `SEED` | int | ❌ | Random seed for reproducibility. If omitted, a random seed is used |

### Validation rules

- `WIDTH` must be between 5 and 100
- `HEIGHT` must be between 5 and 50
- `ENTRY` and `EXIT` must be within bounds and different from each other
- `ENTRY` or `EXIT` cannot fall inside the "42" pattern
- `PERFECT` must be exactly `True` or `False`
- Unknown or duplicate keys raise a configuration error
- `SEED` must be >= 0 if provided

---

## Maze Generation Algorithm

### Algorithm: Recursive Backtracker (Iterative DFS)

The maze is generated using an **iterative Depth-First Search**, also known as the Recursive Backtracker algorithm. It uses an explicit stack instead of recursion to avoid Python's call stack limit on large mazes.

### How it works

1. Start at the entry cell and mark it as visited
2. Push it onto the stack
3. While the stack is not empty:
   - Look at the top cell
   - If it has unvisited neighbors, pick one at random, open the wall between them, mark the neighbor as visited, and push it onto the stack
   - If it has no unvisited neighbors, pop it from the stack (backtrack)
4. When the stack is empty, all cells have been visited — the maze is complete

### Why this algorithm

- **Simple to implement and understand** — the iterative version avoids Python recursion limits that would crash on large mazes
- **Generates perfect mazes** — exactly one path between any two cells (spanning tree)
- **Reproducible** — controlled by a seed via `random.Random(seed)`, isolated from the global random state
- **Easily extended** — the imperfect variant (braiding) is applied as a post-processing step without modifying the core algorithm


---

### Pathfinding — MazeSolver (BFS)

The shortest path from entry to exit is found using **Breadth-First Search (BFS)**.

How it works:

1. Start at the entry cell and add it to a queue
2. For each cell dequeued, check all four directions
3. If the wall in that direction is open and the neighbor has not been visited, add it to the queue and record where it came from
4. When the exit is reached, reconstruct the path by following the parent references back to the entry
5. Convert the coordinate path to a direction string using `N`, `E`, `S`, `W`

BFS guarantees the **shortest path** because it explores cells level by level — the first time it reaches the exit is always via the fewest steps.

---

### Imperfect Mazes — ImperfectMaze (Braiding)

When `PERFECT=False`, the `ImperfectMaze` class applies a **braiding** step after generation.

The goal of this step is to introduce loops by removing selected internal walls while preserving the maze structure.

How it works:

1. Collect all internal closed walls between non-pattern cells as candidates
2. Shuffle the candidate list using the seeded `rng` to keep results reproducible
3. For each candidate wall, evaluate whether it can be removed:
   - The wall must not be a border wall
   - Neither adjacent cell can belong to the "42" pattern
   - Removing the wall must not create a fully open 3×3 area
4. If all checks pass, remove the wall — otherwise skip it
5. Continue until the configured amount of wall removal attempts is completed

The amount of removed walls is controlled using an adaptive probability based on the maze size:
- Small mazes use a higher probability because they have fewer candidate walls
- Larger mazes use a lower probability to avoid destroying the maze structure

The result is an imperfect maze containing loops, where multiple paths may exist between some pairs of cells, making the maze harder to solve visually while preserving important constraints.


## Output File Format

The output file contains:

1. The maze grid — one row per line, one uppercase hex digit per cell
2. A blank line
3. Entry coordinates (`x,y`)
4. Exit coordinates (`x,y`)
5. Shortest path from entry to exit using the letters `N`, `E`, `S`, `W`

Each hex digit encodes which walls are **closed** (bit = 1) or **open** (bit = 0):

| Bit | Direction |
|---|---|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

Example: `F` = `1111` = all walls closed (pattern "42" cells).

### Example output

```
9F3A...
...
1,1
19,14
SSEENWW...
```

---

## Reusable Module — mazegen

The maze generation logic is packaged as a standalone pip-installable module called `mazegen`.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen import MazeGenerator

# Create and generate a perfect maze
gen = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42        # optional — omit for random
)
gen.generate()

# Solve — returns (list of (x,y) coords, direction string)
coords, path_str = gen.solve()

# Export to hex file
gen.export("output_maze.txt")

# Access the raw bitmask map
my_map = gen.my_map  # list[list[int]]
```

### Custom parameters

| Parameter | Type | Description |
|---|---|---|
| `width` | int | Number of columns |
| `height` | int | Number of rows |
| `entry` | tuple[int, int] | Entry coordinates |
| `exit` | tuple[int, int] | Exit coordinates |
| `perfect` | bool | Perfect or imperfect maze |
| `seed` | int or None | Seed for reproducibility |

### Rebuild the package

```bash
python3 -m venv venv_build
source venv_build/bin/activate
make build
deactivate
```

---

## Visual Representation

The maze is rendered in the terminal using ANSI color codes and Unicode block characters. The interactive menu offers the following options:

1. **Re-generate** — generate a new random maze
2. **Show/Hide path** — toggle the solution path visibility
3. **Change color theme** — cycle between color themes (Classic, Neon, Neon Secondary)
4. **Quit**

### Color themes

The ASCII renderer supports different color themes that can be selected during execution.

| Element | Classic | Neon | Neon Secondary |
|---|---|---|---|
| Walls | Blue | Magenta | Yellow |
| Path | Magenta | Yellow | Blue |
| Entry | Green | Green | Green |
| Exit | Red | Red | Red |
| Pattern 42 | Yellow | White | Magenta |

---

## Team and Project Management

### Roles

| Member | Responsibilities |
|---|---|
| rosavela | Parser, pattern_42, renderer, solver, display_ui, imperfect maze, a_maze_ing entry point |
| jreyes-s | Maze models (Cell, Maze), Recursive Backtracker, MazeGenerator, constants, hex exporter |

### Planning

| Week | Plan | Reality |
|---|---|---|
| Week 1 | Parser and maze generator | Parser and initial maze generator structure |
| Week 2 | Renderer and remaining implementations | Renderer, solver, display UI, exporter, imperfect maze |
| Week 3 | Code review, branch merges, docstrings, comments, testing | Code review, merging branches, docstrings, comments, testing and final fixes |

### What worked well

- Communication via Slack was smooth throughout the project
- Clear separation of responsibilities allowed parallel development
- Using a seed from the start made debugging reproducible mazes much easier

### What could be improved

- Defining the internal data structure (bitmask vs objects) and the project tree at the very beginning would have avoided integration friction when merging both parts
- More early integration testing between the generator and renderer would have caught interface mismatches sooner

### Tools used

- **VS Code** — main editor
- **Git** — version control and branch management
- **Slack** — team communication

---

## Resources

### Maze generation

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker explained — Jamis Buck](http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)

### BFS and pathfinding

- [Breadth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)

### Python packaging

- [Python Packaging User Guide](https://packaging.python.org/en/latest/)
- [pyproject.toml reference](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

### How AI was used

AI was used throughout the project as a technical assistant, specifically for:

- **Documentation** — generating and reviewing Google-style docstrings and inline comments in English
- **Code review** — checking for Pythonic style, valid type hints, and flake8/mypy compliance
- **Error cases** — identifying edge cases such as entry/exit inside the "42" pattern, border wall protection in braiding, and 3×3 open area detection
- **Coherence checks** — verifying the hex output format against the subject specification and simulating Moulinette validation
- **Architecture guidance** — discussing the bitmask vs object model trade-offs and the integration between the generator and renderer modules

All AI-generated suggestions were reviewed, tested, and adapted by the team before inclusion in the project.