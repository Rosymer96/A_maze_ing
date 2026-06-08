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
        for line_num, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ConfigError(f"Syntax error in line {line_num}")

            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()

            if key == "WIDTH":
                width = parse_int(value, "WIDTH", line_num)

            elif key == "HEIGHT":
                height = parse_int(value, "HEIGHT", line_num)

            elif key == "ENTRY":
                entry = parse_coords(value, "ENTRY", line_num)

            elif key == "EXIT":
                exit = parse_coords(value, "EXIT", line_num)

            elif key == "OUTPUT_FILE":
                output_file = value

            elif key == "PERFECT":
                if value.lower() not in ("true", "false"):
                    raise ConfigError("PERFECT must be true/false")
                perfect = value.lower() == "true"

            elif key == "SEED":
                seed = parse_int(value, "SEED", line_num)

            else:
                raise ConfigError(f"Unknown key '{key}' in line {line_num}")

    if width is None:
        raise ConfigError("Missing WIDTH in config.txt")
    if height is None:
        raise ConfigError("Missing HEIGHT in config.txt")
    if entry is None:
        raise ConfigError("Missing ENTRY in config.txt")
    if exit is None:
        raise ConfigError("Missing EXIT in config.txt")
    if output_file is None:
        raise ConfigError("Missing OUTPUT_FILE in config.txt")
    if perfect is None:
        raise ConfigError("Missing PERFECT in config.txt")
    if width <= 0 or height <= 0:
        raise ConfigError("Width/Height must be > 0")

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


def parse_int(value: str, key: str, line: int) -> int:
    """
    Convert a string value to an integer with validation.

    Args:
        value (str): The string value to convert.
        key (str): Configuration key name (used for error messages).
        line (int): Line number in the config file (for debugging).

    Returns:
        int: Parsed integer value.

    Raises:
        ConfigError: If the value is not a valid integer.
    """
    if not value.isdigit():
        raise ConfigError(f"{key} must be integer in line {line}")
    return int(value)


def parse_coords(
    value: str,
    key: str,
    line: int
) -> tuple[int, int]:
    """
    Parse coordinate string "x,y" into tuple.

    Parameters
    ----------
    value : str
        Coordinate string (e.g. "3,5").
    key : str
        Configuration key name.
    line : int
        Line number in config file.

    Returns
    -------
    tuple[int, int]
        Parsed (x, y) coordinates.

    Raises
    ------
    ConfigError
        If format is invalid or values are not integers.
    """
    parts = value.split(",")

    if len(parts) != 2:
        raise ConfigError(
            f"{key} must follow format x,y in line {line}"
        )

    x_str, y_str = parts
    if not x_str.strip() or not y_str.strip():
        raise ConfigError(
            f"{key} must follow format x,y in line {line}"
        )

    try:
        x = int(x_str)
        y = int(y_str)
    except ValueError as exc:
        raise ConfigError(
            f"{key} coordinates must be integers "
            f"line {line}"
        ) from exc
    return x, y
