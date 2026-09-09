"""
Orientation
===========

Represents the four compass directions a robot can face, and the
rules for turning left/right and for moving forward.

Keeping this logic in its own class (rather than scattering
if/elif chains through the simulation code) means the "rotate 90
degrees" and "which way is forward" rules live in exactly one place.
"""

from __future__ import annotations

from enum import Enum
from typing import Tuple


class Orientation(Enum):
    """The four cardinal directions a robot can face."""

    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    def turn_right(self) -> "Orientation":
        """Return the orientation after turning 90 degrees clockwise."""
        order = _CLOCKWISE_ORDER
        current_index = order.index(self)
        return order[(current_index + 1) % len(order)]

    def turn_left(self) -> "Orientation":
        """Return the orientation after turning 90 degrees anticlockwise."""
        order = _CLOCKWISE_ORDER
        current_index = order.index(self)
        return order[(current_index - 1) % len(order)]

    def forward_delta(self) -> Tuple[int, int]:
        """
        Return the (dx, dy) change in grid coordinates that results
        from moving one step forward while facing this orientation.

        North corresponds to (x, y) -> (x, y + 1), as specified in
        the problem statement, and the other three directions follow
        the same 90-degree-rotation pattern.
        """
        return _FORWARD_DELTAS[self]


# Defined outside the class body because Enum members can't easily
# reference the enum class itself during its own construction.
_CLOCKWISE_ORDER = [
    Orientation.NORTH,
    Orientation.EAST,
    Orientation.SOUTH,
    Orientation.WEST,
]

_FORWARD_DELTAS = {
    Orientation.NORTH: (0, 1),
    Orientation.EAST: (1, 0),
    Orientation.SOUTH: (0, -1),
    Orientation.WEST: (-1, 0),
}
