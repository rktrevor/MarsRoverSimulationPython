"""
parser
======

Converts the raw text input format described in the challenge into
a :class:`~mars_robots.grid.Grid` and a list of
(:class:`~mars_robots.robot.Robot`, instructions) pairs.

Input format
------------
Line 1: two integers - the upper-right coordinates of the grid
        (lower-left is always 0, 0).
Then, for each robot, two lines:
    - "x y ORIENTATION", e.g. "1 1 E"
    - an instruction string, e.g. "RFRFRFRF"

Blank lines between robots (as in the sample input) are ignored.
"""

from __future__ import annotations

from typing import List, Tuple

from .grid import Grid
from .orientation import Orientation
from .robot import Robot


class InputFormatError(ValueError):
    """Raised when the input text doesn't match the expected format."""


def parse_input(text: str) -> Tuple[Grid, List[Tuple[Robot, str]]]:
    """
    Parse `text` and return a (grid, robots) tuple, where `robots` is
    a list of (Robot, instruction_string) pairs in the order they
    should be processed.
    """
    # Ignore blank lines so the sample input's spacing between robots
    # doesn't need any special handling.
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        raise InputFormatError("Input is empty")

    grid = parse_grid_line(lines[0])

    robots: List[Tuple[Robot, str]] = []
    remaining = lines[1:]

    if len(remaining) % 2 != 0:
        raise InputFormatError(
            "Expected pairs of (position, instructions) lines after the grid size"
        )

    for i in range(0, len(remaining), 2):
        position_line = remaining[i]
        instruction_line = remaining[i + 1]
        robot = parse_robot_line(position_line)
        robots.append((robot, instruction_line))

    return grid, robots


def parse_grid_line(line: str) -> Grid:
    """
    Parse a single "max_x max_y" line into a Grid.

    Exposed separately (not just as an internal helper) so callers
    that gather input line-by-line - e.g. an interactive console
    prompt - can validate and construct the grid without needing to
    build a full multi-line input block first.
    """
    parts = line.split()
    if len(parts) != 2:
        raise InputFormatError(f"Expected 'max_x max_y', got: {line!r}")
    try:
        max_x, max_y = int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise InputFormatError(f"Grid coordinates must be integers: {line!r}") from exc
    return Grid(max_x, max_y)


def parse_robot_line(line: str) -> Robot:
    """
    Parse a single "x y ORIENTATION" line into a Robot.

    Exposed separately for the same reason as `parse_grid_line`.
    """
    parts = line.split()
    if len(parts) != 3:
        raise InputFormatError(f"Expected 'x y ORIENTATION', got: {line!r}")

    x_str, y_str, orientation_str = parts
    try:
        x, y = int(x_str), int(y_str)
    except ValueError as exc:
        raise InputFormatError(f"Robot coordinates must be integers: {line!r}") from exc

    try:
        orientation = Orientation(orientation_str)
    except ValueError as exc:
        raise InputFormatError(f"Unknown orientation '{orientation_str}'") from exc

    return Robot(x=x, y=y, orientation=orientation)
