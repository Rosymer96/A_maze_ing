import os
from maze.renderer import AsciiRenderer, RenderTheme
from maze.parser import Config
from maze.solver import MazeSolver

# ── Datos de prueba ─────────────────────────────────────────────────
# Cuando tengas maze_generator, reemplaza _parse_raw(_RAW) en run() por:
#   my_map = maze_generator.generate(config.width, config.height, config.seed)

RAW = """9515391539551795151151153
EBABAE812853C1412BA812812
96A8416A84545412AC4282C2A
C3A83816A9395384453A82D02
96842A852AC07AAD13A8283C2
C1296C43AAB83AA92AA8686BA
92E853968428444682AC12902
AC3814452FA83FFF82C52C42A
85684117AFC6857FAC1383D06
C53AD043AFFFAFFF856AA8143
91441294297FAFD501142C6BA
AA912AC3843FAFFF82856D52A
842A8692A92B8517C4451552A
816AC384468285293917A9542
C416928513C443A828456C3BA
91416AA92C393A82801553AAA
A81292AA814682C6A8693C6AA
A8442C6C2C1168552C16A9542
86956951692C1455416928552
C545545456C54555545444556"""


# PLACEHOLDER: camino hardcodeado del subject.
# Cuando tengas solver, reemplaza _build_path(...) en run() por:
#   path_coords = solver.solve(my_map, config.entry, config.exit)
path_str = "SWSESWSESWSSSEESEEENEESESEESSSEEESSSEEENNENEE"


directions = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}


def _parse_raw(raw: str) -> list[list[int]]:
    """Convierte el string hex del subject en my_map."""
    my_map = []
    for line in raw.strip().splitlines():
        row = []
        for ch in line:
            row.append(int(ch, 16))
        my_map.append(row)
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
    "Render the maze and print it to the console also the menu."
    #clear_screen()
    print(renderer.render(my_map, entry, exit_))
    print("\033[1;93m" + "═" * 35 + "\033[0m")
    print("\033[1;93m   === Ａ－Ｍａｚｅ－ｉｎｇ ===\033[0m")
    print("\033[1;93m" + "═" * 35 + "\033[0m")
    print()
    print("  \033[1;96m1.\033[0m Re-generar nuevo laberinto\n")
    print("  \033[1;96m2.\033[0m Mostrar/Ocultar camino de solución\n")
    print("  \033[1;96m3.\033[0m Cambiar colores de paredes\n")
    print("  \033[1;96m4.\033[0m Salir\n")
    print("\033[1;93m" + "═" * 35 + "\033[0m")
    if error_msg:  # ← se pinta solo si hay error
        print(f"  \033[1;91m{error_msg}\033[0m")
    print("  Opción (1-4): ", end="", flush=True)

# ── Bucle principal ──────────────────────────────────────────


def run(config: Config) -> None:
    themes = [RenderTheme.classic(), RenderTheme.neon()]
    theme_index = 0

    # PLACEHOLDER — reemplazar cuando estén listos:
    #   my_map      → maze_generator.generate(...)
    #   path_coords → solver.solve(my_map, config.entry, config.exit)
    my_map = _parse_raw(RAW)  # Placeholder para el mapa generado
    print("MY_MAP:", my_map)  # Debug: muestra el mapa en consola
    solver = MazeSolver()
    path_coords, path_str = solver.solve(my_map, config.entry, config.exit)
    print(f"Camino: {path_str}")
    print(f"Pasos:  {len(path_coords)}")
    #path_coords = _build_path(config.entry, path_str)

    renderer = AsciiRenderer(
        theme=themes[theme_index],
        show_path=False,
        path=path_coords,
    )
    error_msg = ""

    while True:
        display_maze(renderer, my_map, config.entry, config.exit, error_msg)
        error_msg = ""  # Aquí podrías actualizar el mensaje de error
        choice = input().strip()
        if choice == "1":
            # Aquí iría la lógica para generar un nuevo laberinto
            # TODO: llamar a maze_generator y actualizar my_map + path_coords
            pass
        elif choice == "2":
            renderer.show_path = not renderer.show_path
        elif choice == "3":
            theme_index = (theme_index + 1) % len(themes)
            renderer.set_theme(themes[theme_index])
            
        elif choice == "4":
            clear_screen()
            print("¡Gracias por jugar a A-Maze-ing!")
            break
        else:
            error_msg = "Invalid option. Please choose between 1 and 4.\n"
