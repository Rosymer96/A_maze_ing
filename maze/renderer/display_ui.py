import os
from maze.renderer import AsciiRenderer, RenderTheme
from maze.parser import Config
from maze.generator import MazeGenerator
from maze.solver import MazeSolver
from maze.exporter import HexExporter


def _convert_and_solve(
    config: Config,
    renderer: AsciiRenderer,
    use_seed: bool = True
) -> list[list[int]]:
    seed_value = config.seed if use_seed else None

    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit=config.exit,
        seed=seed_value
    )
    maze_obj = generator.generate()

    my_map = []
    for y in range(config.height):
        row = []
        for x in range(config.width):
            row.append(int(maze_obj.grid[y][x].walls.value))
        my_map.append(row)

    import maze.utils as pattern_42
    temp_visited = [[False for _ in range(config.width)]
                    for _ in range(config.height)]
    pattern = pattern_42.apply_pattern_42(
        my_map, temp_visited, config.width, config.height)
    if pattern is False:
        print("\033[1;91mThe maze is too small to include the"
              " '42' pattern.\n\033[0m")

    solver = MazeSolver()
    path_coords, path_str = solver.solve(my_map, config.entry, config.exit)
    exporter = HexExporter(maze_obj)
    exporter.write(
        output_file=config.output_file,
        entry=config.entry,
        exit=config.exit,
        path_str=path_str
    )

    renderer.set_path(path_coords)

    return my_map


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def display_maze(
        renderer: AsciiRenderer,
        my_map: list[list[int]],
        entry: tuple[int, int],
        exit_: tuple[int, int],
        error_msg: str = "",
) -> None:
    clear_screen()
    print(renderer.render(my_map, entry, exit_), end="")
    print("\033[1;93m" + "═" * 51 + "\033[0m")
    print("\033[1;93m            === Ａ－Ｍａｚｅ－ｉｎｇ ===\033[0m")
    print("\033[1;93m" + "═" * 51 + "\033[0m")
    print()
    print("  \033[1;96m1.\033[0m Re-generar nuevo laberinto\n")
    print("  \033[1;96m2.\033[0m Mostrar/Ocultar camino de solución\n")
    print("  \033[1;96m3.\033[0m Cambiar colores de paredes\n")
    print("  \033[1;96m4.\033[0m Salir\n")
    print("\033[1;93m" + "═" * 51 + "\033[0m")
    if error_msg:
        print(f"  \033[1;91m{error_msg}\033[0m")
    print("  Opción (1-4): ", end="", flush=True)


def run(config: Config) -> None:
    themes = [RenderTheme.classic(), RenderTheme.neon()]
    theme_index = 0

    renderer = AsciiRenderer(
        theme=themes[theme_index],
    )

    my_map = _convert_and_solve(config, renderer, use_seed=True)
    error_msg = ""
    while True:
        display_maze(renderer, my_map, config.entry, config.exit, error_msg)
        error_msg = ""
        choice = input().strip()

        if choice == "1":
            my_map = _convert_and_solve(config, renderer, use_seed=False)
        elif choice == "2":
            renderer.show_path = not renderer.show_path
        elif choice == "3":
            theme_index = (theme_index + 1) % len(themes)
            renderer.set_theme(themes[theme_index])
        elif choice == "4":
            print("¡Gracias por jugar a A-Maze-ing!")
            break
        else:
            error_msg = "Invalid option. Please choose between 1 and 4.\n"
