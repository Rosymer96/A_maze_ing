import sys
from mazegen import MazeGenerator, MazeGeneratorError
from maze import parse_config, ConfigError, run


def main() -> None:
    """Entry point of the A-Maze-ing program.

    Parses the configuration file, generates the maze, and launches
    the interactive terminal UI.

    Usage:
        python3 a_maze_ing.py config.txt
    """
    if len(sys.argv) != 2:
        print("Uso: python3 a_maze_ing.py <config.txt>", file=sys.stderr)
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
        gen = MazeGenerator(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit=config.exit,
            perfect=config.perfect,
            seed=config.seed,
        )
        gen.generate()
        run(gen, config.output_file)

    except (ConfigError, MazeGeneratorError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nUser interrupted the program. Exiting...", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
