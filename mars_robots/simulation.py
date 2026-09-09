"""
Simulation
==========

Runs a robot's instruction string against a :class:`~mars_robots.grid.Grid`
and reports its final position.

The problem statement notes that "additional command types may be
required in the future". To make that easy, instructions are handled
via a lookup table (character -> handler method) rather than an
if/elif chain, so a new instruction can be added with a single call
to :meth:`Simulation.register_instruction` without touching the core
processing loop.
"""

from __future__ import annotations

from typing import Callable, Dict

from .grid import Grid
from .robot import Robot

# A handler receives the simulation and the robot, and mutates the
# robot's state in place.
InstructionHandler = Callable[["Simulation", Robot], None]


class Simulation:
    """Executes robot instructions against a shared grid."""

    def __init__(self, grid: Grid) -> None:
        self.grid = grid

        # Default instruction set required by the challenge.
        self._instruction_handlers: Dict[str, InstructionHandler] = {
            "L": Simulation._handle_left,
            "R": Simulation._handle_right,
            "F": Simulation._handle_forward,
        }

    def register_instruction(self, letter: str, handler: InstructionHandler) -> None:
        """
        Register a new (or replacement) instruction handler.

        `handler` should be a callable taking (simulation, robot) and
        mutating the robot's state. This is the extension point for
        any future command types.
        """
        self._instruction_handlers[letter] = handler

    def run(self, robot: Robot, instructions: str) -> str:
        """
        Execute `instructions` against `robot` in order, stopping
        early if the robot is lost, and return its final position
        report.
        """
        for letter in instructions:
            if robot.lost:
                # A lost robot no longer responds to instructions.
                break

            handler = self._instruction_handlers.get(letter)
            if handler is None:
                raise ValueError(f"Unknown instruction '{letter}'")

            handler(self, robot)

        return robot.report()

    # -- Built-in instruction handlers -----------------------------------

    @staticmethod
    def _handle_left(simulation: "Simulation", robot: Robot) -> None:
        robot.turn_left()

    @staticmethod
    def _handle_right(simulation: "Simulation", robot: Robot) -> None:
        robot.turn_right()

    @staticmethod
    def _handle_forward(simulation: "Simulation", robot: Robot) -> None:
        grid = simulation.grid
        new_x, new_y = robot.next_position()

        if grid.is_within_bounds(new_x, new_y):
            robot.move_to(new_x, new_y)
            return

        # The instruction would move the robot off the grid.
        if grid.has_scent(robot.x, robot.y):
            # A previous robot was already lost from here - later
            # robots simply ignore the instruction and stay put.
            return

        # Otherwise, the robot is lost. It leaves a scent at the last
        # grid point it occupied before disappearing.
        robot.lost = True
        grid.leave_scent(robot.x, robot.y)
