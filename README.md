# Martian Robots

A solution to the Red Badger "Martian Robots" coding challenge.

## Problem

Robots move around a bounded rectangular grid representing the
surface of Mars, following instructions `L` (turn left), `R` (turn
right), and `F` (move forward). A robot that moves off the edge of
the grid is lost, but leaves a "scent" behind that stops later
robots from being lost at the same point.

Full spec: see the original challenge PDF.

## Requirements

- Python 3.8+ (standard library only, no third-party dependencies)

## Running

Three ways to supply input:

```bash
# 1. From a file
python main.py sample_input.txt

# 2. Piped/redirected input
python main.py < sample_input.txt
cat sample_input.txt | python main.py

# 3. Interactively at the console (run with no file and nothing piped in)
python main.py
```

In interactive mode you're prompted for the grid size, then for each
robot's starting position and instructions in turn. Each robot's
result - including `LOST` if it fell off the grid - is printed as
soon as its instructions are entered. Press Enter on an empty
position line to finish (you don't need to know the robot count in
advance).

```
$ python main.py
Martian Robots - interactive mode
(You can also run 'python main.py <file>' to read input from a file.)

Grid upper-right coordinates 'max_x max_y' (e.g. '5 3'): 5 3
Robot 1 position 'x y ORIENTATION' (e.g. '1 1 E'), or press Enter to finish: 1 1 E
Robot 1 instructions (letters L, R, F): RFRFRFRF
  -> 1 1 E

Robot 2 position 'x y ORIENTATION' (e.g. '1 1 E'), or press Enter to finish: 3 2 N
Robot 2 instructions (letters L, R, F): FRRFLLFFRRFLL
  -> 3 3 N LOST

Robot 3 position 'x y ORIENTATION' (e.g. '1 1 E'), or press Enter to finish:
No more robots entered - finished.
```

Sample input (`sample_input.txt`):

```
5 3
1 1 E
RFRFRFRF

3 2 N
FRRFLLFFRRFLL

0 3 W
LLFFFLFLFL
```

Expected output:

```
1 1 E
3 3 N LOST
2 3 S
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

The test suite includes an end-to-end test that runs the exact
sample input from the challenge and asserts the output matches the
documented sample output line-for-line, unit tests for each class
(`Orientation`, `Grid`, `Robot`, `Simulation`) and the input parser
(including the scent-based "ignore the move" edge case), and tests
for the interactive console prompts in `main.py` (mocking `input()`
to drive the flow and checking that going off the grid is reported
as `LOST` immediately).

## Design

The code is split into one class/module per concept in the problem
statement:

| File                          | Responsibility                                                        |
|--------------------------------|-------------------------------------------------------------------------|
| `mars_robots/orientation.py`  | The four compass directions; turning left/right; forward direction    |
| `mars_robots/robot.py`        | A single robot's position, orientation, and lost state                |
| `mars_robots/grid.py`         | The bounded grid and the set of grid points that have a "scent"       |
| `mars_robots/simulation.py`   | Executes an instruction string for a robot against a grid             |
| `mars_robots/parser.py`       | Parses the raw text input format into `Grid` and `Robot` objects      |
| `main.py`                     | CLI entry point - file, piped stdin, or interactive console prompts   |

**Extensibility for future instructions.** The spec notes that
"additional command types may be required in the future". `Simulation`
handles instructions via a lookup table (`{"L": ..., "R": ..., "F": ...}`)
rather than an `if/elif` chain, and exposes
`Simulation.register_instruction(letter, handler)` so a new
instruction can be added without changing the core processing loop.
`tests/test_mars_robots.py::test_custom_instruction_can_be_registered`
demonstrates this by registering a `B` (backward) instruction.

**Verification.** Correctness is checked at two levels:
1. Unit tests for each class in isolation (turning logic, grid
   bounds, scent tracking, robot report formatting).
2. An end-to-end test that runs the full sample input through the
   parser and simulation and asserts the output matches the sample
   output exactly.

## Possible next steps

Given more time, I'd consider:
- Reading grid/coordinate maxima (50) as validated constraints with
  a clear error message rather than silently trusting the input.
- A `--strict` mode that rejects instruction strings over 100
  characters, per the spec's stated limits.
- Property-based tests (e.g. with `hypothesis`) for the turning
  logic, since turning left/right four times should always return to
  the original orientation.
