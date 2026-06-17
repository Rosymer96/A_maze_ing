from collections import deque


class MazeSolver:
    def solve(
            self,
            my_map: list[list[int]],
            entry: tuple[int, int],
            exit: tuple[int, int]
    ) -> tuple[list[tuple[int, int]], str]:
        """
        Find the shorest path between entry and exit
        Args:
        (completar...)
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
            (8, -1, 0, "O")
        ]

        found = False
        while path:
            cx, cy = path.popleft()
            if (cx, cy) == exit:
                found = True
                break

            bits = my_map[cy][cx]

            for bit, dx, dy, _ in directions:
                nx, ny = cx + dx, cy + dy

            # Verificar si esta en el mapa
                if not (0 <= nx < width and 0 <= ny < height):
                    continue

                # Verificar si ya esta visitada
                if visited[ny][nx]:
                    continue

                # hay pared en esa direccion:
                if bits & bit:
                    continue

            # Si la siguiente celda es accesible
                visited[ny][nx] = True
                parent[(nx, ny)] = (cx, cy)
                path.append((nx, ny))

    #   Camino hacia atras
        if not found:
            return [], ""

        coords: list[tuple[int, int]] = []
        current: tuple[int, int] | None = exit

        while current is not None:
            coords.append(current)
            current = parent.get(current)
        coords.reverse()

        # Convertir a coordenadas
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
