"""
Grid
====

Represents the rectangular, bounded surface of Mars that robots move
around on.

The grid is responsible for two things:

1. Knowing whether a given coordinate is within its bounds.
2. Remembering the "scent" left behind at any grid point from which a
   robot has previously fallen off the edge, so that later robots
   don't repeat the same mistake.
"""

from __future__ import annotations

from typing import Set, Tuple


class Grid:
    """A bounded rectangular grid with lower-left corner at (0, 0)."""

    def __init__(self, max_x: int, max_y: int) -> None:
        """
        Create a grid spanning from (0, 0) to (max_x, max_y) inclusive.
        """
        self.max_x = max_x
        self.max_y = max_y

        # Grid points from which a robot has previously been lost.
        self._scents: Set[Tuple[int, int]] = set()

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) lies within the grid, inclusive."""
        return 0 <= x <= self.max_x and 0 <= y <= self.max_y

    def has_scent(self, x: int, y: int) -> bool:
        """Return True if a robot has previously been lost from (x, y)."""
        return (x, y) in self._scents

    def leave_scent(self, x: int, y: int) -> None:
        """Record that a robot was lost from grid point (x, y)."""
        self._scents.add((x, y))
