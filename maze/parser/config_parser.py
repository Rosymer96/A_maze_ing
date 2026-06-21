from dataclasses import dataclass
from typing import Tuple
import os


class ConfigError(Exception):
    """Configuration error."""
    pass


@dataclass
class Config:
    """Maze configuration."""

    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def parse_config(file_path: str) -> Config:
    """
    Parse and validate config file.

    Args:
        file_path: path to config file

    Returns:
        Config object

    Raises:
        ConfigError if invalid config
    """

    if not os.path.exists(file_path):
        raise ConfigError(f"File not found: {file_path}")

    width: int | None = None
    height: int | None = None
    entry: Tuple[int, int] | None = None
    exit: Tuple[int, int] | None = None
    output_file: str | None = None
    perfect: bool | None = None
    seed: int | None = None

    with open(file_path, "r") as file:
        seen_keys: set[str] = set()

        for line_num, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ConfigError(
                    f"Invalid configuration at line {line_num}:"
                    f" expected format 'KEY=VALUE'")

            key, value = line.split("=", 1)
            key = key.strip().upper()
            if key in seen_keys:
                raise ConfigError(f"Duplicate key '{key}' at line {line_num}")
            seen_keys.add(key)

            value = value.strip()

            if key == "WIDTH":
                width = parse_int(value, "WIDTH")

            elif key == "HEIGHT":
                height = parse_int(value, "HEIGHT")

            elif key == "ENTRY":
                entry = parse_coords(value, "ENTRY")

            elif key == "EXIT":
                exit = parse_coords(value, "EXIT")

            elif key == "OUTPUT_FILE":
                output_file = value

            elif key == "PERFECT":
                if value not in ("True", "False"):
                    raise ConfigError(f"Invalid value for PERFECT: expected"
                                      f" 'True' or 'False', got '{value}'")
                perfect = value == "True"

            elif key == "SEED":
                seed = parse_int(value, "SEED")

            else:
                raise ConfigError(
                    f"Unknown configuration key '{key}' in line {line_num}"
                )

    if width is None:
        raise ConfigError("Missing mandatory key 'WIDTH'")
    if height is None:
        raise ConfigError("Missing mandatory key 'HEIGHT'")
    if entry is None:
        raise ConfigError("Missing mandatory key 'ENTRY'")
    if exit is None:
        raise ConfigError("Missing mandatory key 'EXIT'")
    if output_file is None:
        raise ConfigError("Missing mandatory key 'OUTPUT_FILE'")
    if perfect is None:
        raise ConfigError("Missing mandatory key 'PERFECT'")

    if seed is not None and seed < 0:
        raise ConfigError("Seed must be >= 0")
    if width <= 0 or width > 100:
        raise ConfigError("Width must be > 0 and <= 100")

    if height <= 0 or height > 50:
        raise ConfigError("Height must be > 0 and <= 50")

    if entry == exit:
        raise ConfigError("Entry and Exit cannot be the same")

    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ConfigError("Entry out of bounds")

    if not (0 <= exit[0] < width and 0 <= exit[1] < height):
        raise ConfigError("Exit out of bounds")

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )


def parse_int(value: str, key: str) -> int:
    """
    Convert a string value to an integer with validation.

    Args:
        value (str): The string value to convert.
        key (str): Configuration key name (used for error messages).

    Returns:
        int: Parsed integer value.

    Raises:
        ConfigError: If the value is not a valid integer.
    """
    if not value.isdigit():
        raise ConfigError(
            f"Invalid value for {key}: expected integer, got '{value}'"
            )
    return int(value)


def parse_coords(
    value: str,
    key: str
) -> tuple[int, int]:
    """
    Parse coordinate string "x,y" into tuple.

    Args:
    value : Coordinate string (e.g. "3,5").
    key : Configuration key name.

    Returns:
        Tuple containing (x, y).

    Raises:
        ConfigError: If format is invalid.
    """
    parts = value.split(",")

    if len(parts) != 2:
        raise ConfigError(
            f"Invalid {key} format: expected 'x,y', got {value}"
        )

    x_str, y_str = parts
    if not x_str.strip() or not y_str.strip():
        raise ConfigError(
            f"Invalid {key} format: expected 'x,y', got {value}"
        )

    try:
        x = int(x_str)
        y = int(y_str)
    except ValueError as exc:
        raise ConfigError(
            f"Invalid {key}: x and y must be integers"
        ) from exc
    return x, y
