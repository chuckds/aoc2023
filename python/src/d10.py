"""
Advent Of Code 2023 Day 10
"""

from __future__ import annotations

import enum
from pathlib import Path
from typing import NamedTuple
import utils


class Direction(enum.Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    WEST = (-1, 0)
    EAST = (1, 0)


class Coord(NamedTuple):
    col: int
    line: int

    def in_direction(self, direction: Direction) -> Coord:
        return Coord(self.col + direction.value[0], self.line + direction.value[1])


CHAR_TO_CONNECTIONS = {
    "|": (Direction.NORTH, Direction.SOUTH),
    "-": (Direction.EAST, Direction.WEST),
    "L": (Direction.NORTH, Direction.EAST),
    "J": (Direction.NORTH, Direction.WEST),
    "7": (Direction.SOUTH, Direction.WEST),
    "F": (Direction.SOUTH, Direction.EAST),
}


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p2 = 0
    start = None
    coord_to_conns = {}
    for line_num, line in enumerate(input_file.read_text().splitlines()):
        for col_num, char in enumerate(line):
            coord = Coord(col_num, line_num)
            if char == "S":
                start = coord
            else:
                coord_to_conns[coord] = {
                    coord.in_direction(dir)
                    for dir in CHAR_TO_CONNECTIONS.get(char, ())
                }
    assert start is not None
    # Find a coord that connects to start
    for a_dir in Direction:
        start_adjcent = start.in_direction(a_dir)
        if start in coord_to_conns[start_adjcent]:
            break  # start_adjcent connects to start so walk from here
    coord, prev = start_adjcent, start
    steps = 1  # Already moved from start
    while coord != start:
        steps += 1
        coord, prev = next(c for c in coord_to_conns[coord] if c != prev), coord

    return (steps // 2, p2)


if __name__ == "__main__":
    utils.per_day_main(p1p2, example_only=False)
