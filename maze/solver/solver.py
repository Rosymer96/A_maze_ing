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

        print(height)
        visited: list[list[bool]] = []
        for _ in range(height):
            vis = []
            for _ in range(width):
                vis += [False]
            visited += [vis]
        
        parent: dict[tuple[int, int], tuple[int, int] | None] = {}
        path: deque[tuple[int, int]] = deque([entry])
        visited[[entry[1]][entry[0]]] = True
        parent[entry] = None
        #Definir los caminos 
        directions = [
            (1, 0, -1, "N"),
            (2, 1, 0, "E"),
            (4, 0, 1, "S"),
            (8, -1, 0, "O")
        ]
        #Solver BFS





    






def main():
    solver = MazeSolver()
    print(solver.solve([[1, 4, 6], [2, 5, 8]]))



if __name__ == "__main__":
    main()
