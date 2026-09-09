"""
Tests for the interactive console mode in main.py.

These mock builtins.input to drive the prompts programmatically and
capture stdout to check the printed results, including that a robot
going off the grid is reported as LOST immediately.
"""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


class InteractiveModeTests(unittest.TestCase):
    def _run_interactive(self, inputs):
        """
        Run main._run_interactively() with a scripted sequence of
        `inputs` fed to input(), and return everything printed to
        stdout as a single string.
        """
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                main._run_interactively()
        return output.getvalue()

    def test_sample_scenario_matches_expected_output(self):
        inputs = [
            "5 3",  # grid size
            "1 1 E", "RFRFRFRF",
            "3 2 N", "FRRFLLFFRRFLL",
            "0 3 W", "LLFFFLFLFL",
            "",  # finish
        ]
        output = self._run_interactive(inputs)

        self.assertIn("-> 1 1 E", output)
        self.assertIn("-> 3 3 N LOST", output)
        self.assertIn("-> 2 3 S", output)

    def test_robot_moving_off_grid_reports_lost_immediately(self):
        inputs = [
            "5 3",  # grid size
            "5 3 N", "F",  # one step off the top edge
            "",  # finish
        ]
        output = self._run_interactive(inputs)
        self.assertIn("-> 5 3 N LOST", output)

    def test_invalid_grid_line_is_reprompted(self):
        inputs = [
            "not a grid",  # invalid, should be rejected
            "5 3",  # valid, accepted on retry
            "",  # finish immediately, no robots
        ]
        output = self._run_interactive(inputs)
        self.assertIn("Invalid grid size", output)
        self.assertIn("No more robots entered", output)

    def test_invalid_robot_position_is_reprompted(self):
        inputs = [
            "5 3",  # grid size
            "bad position",  # invalid, should be rejected
            "1 1 E", "F",  # valid, accepted on retry
            "",  # finish
        ]
        output = self._run_interactive(inputs)
        self.assertIn("Invalid position", output)
        self.assertIn("-> 2 1 E", output)

    def test_empty_position_line_ends_input_with_no_robots(self):
        output = self._run_interactive(["5 3", ""])
        self.assertIn("No more robots entered", output)
        self.assertNotIn("->", output)


if __name__ == "__main__":
    unittest.main()
