"""
Advent Of Code 2023 Day 17
"""

from __future__ import annotations

import bisect
import enum
from pathlib import Path
from typing import NamedTuple

import utils


class Direction(enum.Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    WEST = (-1, 0)
    EAST = (1, 0)


DIR_TO_LEFT = {dir: Direction((-1 * dir.value[1], dir.value[0]))
               for dir in Direction}
DIR_TO_RIGHT = {dir: Direction((dir.value[1], -1 * dir.value[0]))
                for dir in Direction}


class Coord(NamedTuple):
    col: int
    line: int

    def in_direction(self, direction: Direction) -> Coord:
        return Coord(self.col + direction.value[0], self.line + direction.value[1])


def in_bounds(loc: Coord, size: int) -> bool:
    return 0 <= loc[0] < size and 0 <= loc[1] < size


def next_dirs_p1(prev_dir: Direction, num_straights: int) -> tuple[Direction, ...]:
    if num_straights == 3:
        return (DIR_TO_LEFT[prev_dir], DIR_TO_RIGHT[prev_dir])
    return (DIR_TO_LEFT[prev_dir], DIR_TO_RIGHT[prev_dir], prev_dir)


def next_dirs_p2(prev_dir: Direction, num_straights: int) -> tuple[Direction, ...]:
    if num_straights == 10:
        return (DIR_TO_LEFT[prev_dir], DIR_TO_RIGHT[prev_dir])
    if num_straights < 4:
        return (prev_dir,)
    else:
        return (DIR_TO_LEFT[prev_dir], DIR_TO_RIGHT[prev_dir], prev_dir)


def min_heat_loss(grid: list[list[int]], start: Coord, end: Coord, p2: bool) -> int:
    n_dir = next_dirs_p2 if p2 else next_dirs_p1
    to_check = [((start, 0, Direction.SOUTH), 0), ((start, 0, Direction.EAST), 0)]
    visited = set()
    size = len(grid[0])
    while to_check:
        walk_state, heat_loss = to_check.pop()
        if walk_state in visited:
            continue
        visited.add(walk_state)
        coord, num_straights, prev_dir = walk_state
        if coord == end:
            return heat_loss
        dirs = n_dir(prev_dir, num_straights)
        for new_dir in dirs:
            new_loc = coord.in_direction(new_dir)
            if not in_bounds(new_loc, size):
                continue
            new_num_straights = 1
            if new_dir == prev_dir:
                new_num_straights += num_straights
            walk_state = (new_loc, new_num_straights, new_dir)
            if walk_state in visited:
                continue
            new_heat_loss = grid[new_loc.line][new_loc.col] + heat_loss
            bisect.insort(to_check, (walk_state, new_heat_loss), key=lambda x: -1 * x[1])
    return 0


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    grid = [
        [int(char) for char in line]
        for line in input_file.read_text().splitlines()
    ]

    return (
        min_heat_loss(grid, Coord(0, 0), Coord(len(grid[0]) - 1, len(grid[0]) - 1), False),
        min_heat_loss(grid, Coord(0, 0), Coord(len(grid[0]) - 1, len(grid[0]) - 1), True)
    )


if __name__ == "__main__":
    utils.per_day_main(p1p2)
