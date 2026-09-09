"""
mars_robots
===========

A small simulation package for the "Martian Robots" coding challenge.

The package is deliberately split into small, single-responsibility
modules so that each concept in the problem statement maps onto one
class:

- :class:`mars_robots.orientation.Orientation` - the four compass
  directions and the rules for turning/moving.
- :class:`mars_robots.robot.Robot` - a single robot's mutable state
  (position, orientation, lost flag).
- :class:`mars_robots.grid.Grid` - the bounded rectangular surface of
  Mars, including the "scent" left by robots that fall off the edge.
- :class:`mars_robots.simulation.Simulation` - runs a robot's
  instruction string against a grid and reports the final position.
- :mod:`mars_robots.parser` - turns the raw text input format into
  the objects above.
"""

from .orientation import Orientation
from .robot import Robot
from .grid import Grid
from .simulation import Simulation

__all__ = ["Orientation", "Robot", "Grid", "Simulation"]
