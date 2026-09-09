"""
Tests for the mars_robots package.

Run with:
    python -m unittest discover -s tests -v
or simply:
    python -m unittest
"""

import unittest

from mars_robots.grid import Grid
from mars_robots.orientation import Orientation
from mars_robots.parser import InputFormatError, parse_input
from mars_robots.robot import Robot
from mars_robots.simulation import Simulation


class OrientationTests(unittest.TestCase):
    def test_turn_right_cycles_clockwise(self):
        self.assertEqual(Orientation.NORTH.turn_right(), Orientation.EAST)
        self.assertEqual(Orientation.EAST.turn_right(), Orientation.SOUTH)
        self.assertEqual(Orientation.SOUTH.turn_right(), Orientation.WEST)
        self.assertEqual(Orientation.WEST.turn_right(), Orientation.NORTH)

    def test_turn_left_cycles_anticlockwise(self):
        self.assertEqual(Orientation.NORTH.turn_left(), Orientation.WEST)
        self.assertEqual(Orientation.WEST.turn_left(), Orientation.SOUTH)
        self.assertEqual(Orientation.SOUTH.turn_left(), Orientation.EAST)
        self.assertEqual(Orientation.EAST.turn_left(), Orientation.NORTH)

    def test_forward_delta_matches_spec(self):
        # "The direction North corresponds to (x, y) -> (x, y+1)"
        self.assertEqual(Orientation.NORTH.forward_delta(), (0, 1))
        self.assertEqual(Orientation.SOUTH.forward_delta(), (0, -1))
        self.assertEqual(Orientation.EAST.forward_delta(), (1, 0))
        self.assertEqual(Orientation.WEST.forward_delta(), (-1, 0))


class GridTests(unittest.TestCase):
    def test_bounds_inclusive(self):
        grid = Grid(5, 3)
        self.assertTrue(grid.is_within_bounds(0, 0))
        self.assertTrue(grid.is_within_bounds(5, 3))
        self.assertFalse(grid.is_within_bounds(6, 3))
        self.assertFalse(grid.is_within_bounds(-1, 0))

    def test_scent_tracking(self):
        grid = Grid(5, 3)
        self.assertFalse(grid.has_scent(3, 3))
        grid.leave_scent(3, 3)
        self.assertTrue(grid.has_scent(3, 3))


class RobotTests(unittest.TestCase):
    def test_report_without_lost(self):
        robot = Robot(1, 1, Orientation.EAST)
        self.assertEqual(robot.report(), "1 1 E")

    def test_report_when_lost(self):
        robot = Robot(3, 3, Orientation.NORTH, lost=True)
        self.assertEqual(robot.report(), "3 3 N LOST")

    def test_next_position_does_not_mutate(self):
        robot = Robot(1, 1, Orientation.NORTH)
        next_pos = robot.next_position()
        self.assertEqual(next_pos, (1, 2))
        self.assertEqual((robot.x, robot.y), (1, 1))


class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(5, 3)
        self.simulation = Simulation(self.grid)

    def test_robot_stays_on_grid(self):
        robot = Robot(1, 1, Orientation.EAST)
        result = self.simulation.run(robot, "RFRFRFRF")
        self.assertEqual(result, "1 1 E")
        self.assertFalse(robot.lost)

    def test_robot_gets_lost_and_leaves_scent(self):
        robot = Robot(3, 2, Orientation.NORTH)
        result = self.simulation.run(robot, "FRRFLLFFRRFLL")
        self.assertEqual(result, "3 3 N LOST")
        self.assertTrue(self.grid.has_scent(3, 3))

    def test_scent_prevents_second_robot_from_being_lost_at_same_spot(self):
        # First robot is lost from (3, 3), leaving a scent there.
        first = Robot(3, 2, Orientation.NORTH)
        self.simulation.run(first, "FRRFLLFFRRFLL")
        self.assertTrue(self.grid.has_scent(3, 3))

        # Second robot approaches the same edge; the "off grid" move
        # should be ignored rather than losing the robot.
        second = Robot(0, 3, Orientation.WEST)
        result = self.simulation.run(second, "LLFFFLFLFL")
        self.assertEqual(result, "2 3 S")
        self.assertFalse(second.lost)

    def test_unknown_instruction_raises(self):
        robot = Robot(0, 0, Orientation.NORTH)
        with self.assertRaises(ValueError):
            self.simulation.run(robot, "X")

    def test_custom_instruction_can_be_registered(self):
        # Demonstrates the extension point for future command types.
        robot = Robot(0, 0, Orientation.NORTH)

        def handle_backward(simulation, robot):
            dx, dy = robot.orientation.forward_delta()
            robot.move_to(robot.x - dx, robot.y - dy)

        self.simulation.register_instruction("B", handle_backward)
        # Move forward then back should return to the start.
        result = self.simulation.run(robot, "FB")
        self.assertEqual(result, "0 0 N")


class ParserTests(unittest.TestCase):
    def test_parses_grid_size(self):
        grid, robots = parse_input("5 3\n1 1 E\nF\n")
        self.assertEqual((grid.max_x, grid.max_y), (5, 3))
        self.assertEqual(len(robots), 1)

    def test_ignores_blank_lines_between_robots(self):
        text = "5 3\n1 1 E\nF\n\n0 3 W\nL\n"
        grid, robots = parse_input(text)
        self.assertEqual(len(robots), 2)

    def test_rejects_malformed_grid_line(self):
        with self.assertRaises(InputFormatError):
            parse_input("not a grid\n1 1 E\nF\n")

    def test_rejects_unknown_orientation(self):
        with self.assertRaises(InputFormatError):
            parse_input("5 3\n1 1 Q\nF\n")


class EndToEndSampleTests(unittest.TestCase):
    """
    Runs the full sample input from the challenge document and checks
    it produces exactly the documented sample output.
    """

    SAMPLE_INPUT = (
        "5 3\n"
        "1 1 E\n"
        "RFRFRFRF\n"
        "\n"
        "3 2 N\n"
        "FRRFLLFFRRFLL\n"
        "\n"
        "0 3 W\n"
        "LLFFFLFLFL\n"
    )

    EXPECTED_OUTPUT = [
        "1 1 E",
        "3 3 N LOST",
        "2 3 S",
    ]

    def test_sample_input_produces_sample_output(self):
        grid, robots = parse_input(self.SAMPLE_INPUT)
        simulation = Simulation(grid)

        results = [simulation.run(robot, instructions) for robot, instructions in robots]

        self.assertEqual(results, self.EXPECTED_OUTPUT)


if __name__ == "__main__":
    unittest.main()
