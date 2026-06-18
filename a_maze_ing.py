import sys
from mazegen import parse_config, ConfigError, run


def main() -> None:
    """Entry point del programa."""
    if len(sys.argv) != 2:
        print("Uso: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
        run(config)
    except ConfigError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
