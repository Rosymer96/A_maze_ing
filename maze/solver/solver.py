from collections import deque


class MazeSolver:
    """Solve a maze using breadth-first search (BFS)."""

    def solve(
            self,
            my_map: list[list[int]],
            entry: tuple[int, int],
            exit_: tuple[int, int]
    ) -> tuple[list[tuple[int, int]], str]:
        """Find the shortest path between entry and exit.

        Args:
            my_map: Maze represented as a grid of wall bitmasks.
            entry: Starting cell coordinates (x, y).
            exit_: Target cell coordinates (x, y).

        Returns:
            A tuple containing:
                - List of coordinates representing the path.
                - String encoding of movement directions.

        Raises:
            ValueError: If the maze is invalid or empty.
        """

        height = len(my_map)
        width = len(my_map[0])

        visited: list[list[bool]] = []
        for _ in range(height):
            vis = []
            for _ in range(width):
                vis += [False]
            visited += [vis]

        parent: dict[tuple[int, int], tuple[int, int] | None] = {}
        path: deque[tuple[int, int]] = deque([entry])
        visited[entry[1]][entry[0]] = True
        parent[entry] = None

        directions = [
            (1, 0, -1, "N"),
            (2, 1, 0, "E"),
            (4, 0, 1, "S"),
            (8, -1, 0, "W")
        ]

        found = False

        while path:
            cx, cy = path.popleft()
            if (cx, cy) == exit_:
                found = True
                break

            bits = my_map[cy][cx]

            for bit, dx, dy, _ in directions:
                nx, ny = cx + dx, cy + dy

                # Check if the next cell is inside the map
                if not (0 <= nx < width and 0 <= ny < height):
                    continue

                # Check if the cell has already been visited
                if visited[ny][nx]:
                    continue

                # Check if there is a wall in this direction
                if bits & bit:
                    continue

                # If the next cell is accessible, add it to the queue
                visited[ny][nx] = True
                parent[(nx, ny)] = (cx, cy)
                path.append((nx, ny))

        # Reconstruct path backwards from exit to entry
        if not found:
            return [], ""

        coords: list[tuple[int, int]] = []
        current: tuple[int, int] | None = exit_

        while current is not None:
            coords.append(current)
            current = parent.get(current)
        coords.reverse()

        # Convert path to movement directions
        letters: list[str] = []
        for i in range(len(coords) - 1):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            dx, dy = x2 - x1, y2 - y1

            for _, ddx, ddy, letter in directions:
                if ddx == dx and ddy == dy:
                    letters.append(letter)
                    break
        return coords, "".join(letters)
