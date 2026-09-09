"""
Robot
=====

Represents a single robot's state on the grid: its coordinates, the
direction it is facing, and whether it has fallen off the edge.

This class only knows about its own state - it does not know
anything about grid boundaries or other robots. That logic belongs
to :class:`mars_robots.grid.Grid` and
:class:`mars_robots.simulation.Simulation`, which keeps each class
focused on a single responsibility.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .orientation import Orientation


@dataclass
class Robot:
    """A robot with a position, an orientation, and a lost flag."""

    x: int
    y: int
    orientation: Orientation
    lost: bool = False

    def turn_left(self) -> None:
        """Rotate the robot 90 degrees anticlockwise on the spot."""
        self.orientation = self.orientation.turn_left()

    def turn_right(self) -> None:
        """Rotate the robot 90 degrees clockwise on the spot."""
        self.orientation = self.orientation.turn_right()

    def next_position(self) -> Tuple[int, int]:
        """
        Return the (x, y) coordinate the robot would occupy if it
        moved one step forward, without actually moving it.
        """
        dx, dy = self.orientation.forward_delta()
        return self.x + dx, self.y + dy

    def move_to(self, x: int, y: int) -> None:
        """Move the robot to the given coordinates."""
        self.x, self.y = x, y

    def report(self) -> str:
        """
        Return the final position report for this robot, in the
        format required by the challenge, e.g. "1 1 E" or
        "3 3 N LOST".
        """
        report = f"{self.x} {self.y} {self.orientation.value}"
        if self.lost:
            report += " LOST"
        return report
