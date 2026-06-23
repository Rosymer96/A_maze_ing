import os
from maze.renderer import AsciiRenderer, RenderTheme
from mazegen import MazeGenerator, MazeGeneratorError


def _generate_and_solve_maze(
    gen: MazeGenerator,
    renderer: AsciiRenderer,
    output_file: str,
) -> list[list[int]]:
    """Generate maze, solve it, and export results.

    Returns:
        2D grid representation of the maze.
    """
    path_coords, _ = gen.solve()

    renderer.set_path(path_coords)
    gen.export(output_file)

    return gen.my_map


def clear_screen() -> None:
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_maze(
        renderer: AsciiRenderer,
        my_map: list[list[int]],
        entry: tuple[int, int],
        exit_: tuple[int, int],
        error_msg: str = "",
) -> None:
    """Render maze and UI menu in terminal."""
    clear_screen()
    print()
    print(renderer.render(my_map, entry, exit_), end="")
    print()
    print("\033[1;93m" + "═" * 51 + "\033[0m")
    print("\033[1;93m            === Ａ－Ｍａｚｅ－ｉｎｇ ===\033[0m")
    print("\033[1;93m" + "═" * 51 + "\033[0m")
    print()
    print("  \033[1;96m1.\033[0m Re-generate a new maze\n")
    print("  \033[1;96m2.\033[0m Show/Hide solution path\n")
    print("  \033[1;96m3.\033[0m Change color theme\n")
    print("  \033[1;96m4.\033[0m Exit\n")
    print("\033[1;93m" + "═" * 51 + "\033[0m")
    if error_msg:
        print(f"  \033[1;91m{error_msg}\033[0m")
    print("  Option (1-4): ", end="", flush=True)


def run(gen: MazeGenerator, output_file: str) -> None:
    """
    Run interactive ASCII maze application.

    Args:
        gen: MazeGenerator instance.
        output_file: Path to the output file.

    Raises:
        MazeGeneratorError: If maze generation fails.
    """
    themes = [
        RenderTheme.classic(),
        RenderTheme.neon(),
        RenderTheme.neon_sec()
    ]
    theme_index = 0

    renderer = AsciiRenderer(
        theme=themes[theme_index],
    )

    my_map = _generate_and_solve_maze(gen, renderer, output_file)
    error_msg = ""
    while True:
        print()
        display_maze(renderer, my_map, gen.entry, gen.exit, error_msg)
        error_msg = ""
        choice = input().strip()

        if choice == "1":
            try:
                gen = MazeGenerator(
                    width=gen.width,
                    height=gen.height,
                    entry=gen.entry,
                    exit=gen.exit,
                    perfect=gen.perfect,
                    seed=None
                )
                gen.generate()
                my_map = _generate_and_solve_maze(gen, renderer, output_file)
            except MazeGeneratorError as e:
                error_msg = str(e)

        elif choice == "2":
            renderer.show_path = not renderer.show_path

        elif choice == "3":
            theme_index = (theme_index + 1) % len(themes)
            renderer.set_theme(themes[theme_index])

        elif choice == "4":
            print("Thanks for playing A-Maze-ing!")
            break

        else:
            error_msg = "Invalid option. Please choose between 1 and 4.\n"
