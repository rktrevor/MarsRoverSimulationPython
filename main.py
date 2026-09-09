#!/usr/bin/env python3
"""
main
====

Command-line entry point for the Martian Robots simulation.

Three ways to supply input are supported:

1. From a file:
       python main.py sample_input.txt

2. Piped/redirected input (non-interactive):
       python main.py < sample_input.txt
       cat sample_input.txt | python main.py

3. Interactively at the console, with prompts:
       python main.py
       (run with no file argument and nothing piped in - you'll be
       prompted to type the grid size and each robot in turn)

For each robot, its final position and orientation is printed, e.g.
"1 1 E", followed by " LOST" if it fell off the edge of the grid,
e.g. "3 3 N LOST".
"""

import sys

from mars_robots.grid import Grid
from mars_robots.parser import InputFormatError, parse_grid_line, parse_input, parse_robot_line
from mars_robots.simulation import Simulation


def main() -> None:
    if len(sys.argv) > 1:
        _run_from_file(sys.argv[1])
    elif sys.stdin.isatty():
        # Nothing was piped in and no file was given - prompt the
        # user for input at the console.
        _run_interactively()
    else:
        _run_from_text(sys.stdin.read())


def _run_from_file(path: str) -> None:
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    _run_from_text(text)


def _run_from_text(text: str) -> None:
    """Parse a full block of input text and print each robot's result."""
    try:
        grid, robots = parse_input(text)
    except InputFormatError as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)
        sys.exit(1)

    simulation = Simulation(grid)
    for robot, instructions in robots:
        print(simulation.run(robot, instructions))


def _run_interactively() -> None:
    """
    Prompt the user for the grid size and each robot in turn,
    printing every robot's result (including LOST) as soon as its
    instructions are entered.

    An empty line at the "position" prompt finishes input, so the
    user doesn't need to know the robot count in advance.
    """
    print("Martian Robots - interactive mode")
    print("(You can also run 'python main.py <file>' to read input from a file.)")
    print()

    grid = _prompt_for_grid()
    simulation = Simulation(grid)

    robot_number = 1
    while True:
        position_line = input(
            f"Robot {robot_number} position 'x y ORIENTATION' "
            f"(e.g. '1 1 E'), or press Enter to finish: "
        ).strip()

        if not position_line:
            break

        try:
            robot = parse_robot_line(position_line)
        except InputFormatError as exc:
            print(f"  Invalid position: {exc}. Try again.")
            continue

        instructions = input(
            f"Robot {robot_number} instructions (letters L, R, F): "
        ).strip()

        result = simulation.run(robot, instructions)
        print(f"  -> {result}")
        print()

        robot_number += 1

    print("No more robots entered - finished.")


def _prompt_for_grid() -> Grid:
    """Repeatedly prompt until a valid grid size line is entered."""
    while True:
        line = input(
            "Grid upper-right coordinates 'max_x max_y' (e.g. '5 3'): "
        ).strip()
        try:
            return parse_grid_line(line)
        except InputFormatError as exc:
            print(f"  Invalid grid size: {exc}. Try again.")


if __name__ == "__main__":
    main()
