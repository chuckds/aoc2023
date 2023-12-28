"""
Advent Of Code 2023 Day 16
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

import utils


class Direction(enum.Enum):
    NORTH = (0, 1)
    SOUTH = (0, -1)
    WEST = (-1, 0)
    EAST = (1, 0)


DIR_TO_LEFT = {dir: Direction((-1 * dir.value[1], dir.value[0])) for dir in Direction}
DIR_TO_RIGHT = {dir: Direction((dir.value[1], -1 * dir.value[0])) for dir in Direction}


class Coord(NamedTuple):
    col: int
    line: int

    def in_direction(self, direction: Direction) -> Coord:
        return Coord(self.col + direction.value[0], self.line + direction.value[1])


@dataclass
class MirrorGrid:
    grid: dict[Coord, str] = field(default_factory=dict)
    size: int = 0

    def in_grid(self, a_coord: Coord) -> bool:
        return 0 <= a_coord[0] < self.size and 0 <= a_coord[1] < self.size


def light_beam(location: Coord, in_dir: Direction, mirror_grid: MirrorGrid) -> int:
    to_check = set([(location, in_dir)])
    seen = set()
    energized = set()
    while to_check:
        location, in_dir = to_check.pop()
        if not mirror_grid.in_grid(location) or (location, in_dir) in seen:
            continue
        energized.add(location)
        seen.add((location, in_dir))
        char = mirror_grid.grid.get(location)
        if char:
            new_dirs: tuple[Direction, ...] = ()
            if char == "|":
                if in_dir in (Direction.WEST, Direction.EAST):
                    new_dirs = (Direction.NORTH, Direction.SOUTH)
                else:
                    new_dirs = (in_dir,)
            elif char == "-":
                if in_dir in (Direction.NORTH, Direction.SOUTH):
                    new_dirs = (Direction.EAST, Direction.WEST)
                else:
                    new_dirs = (in_dir,)
            elif char == "\\":
                new_dirs = (
                    DIR_TO_RIGHT[in_dir]
                    if in_dir in (Direction.WEST, Direction.EAST)
                    else DIR_TO_LEFT[in_dir],
                )
            elif char == "/":
                new_dirs = (
                    DIR_TO_LEFT[in_dir]
                    if in_dir in (Direction.WEST, Direction.EAST)
                    else DIR_TO_RIGHT[in_dir],
                )
        else:
            new_dirs = (in_dir,)
        for new_dir in new_dirs:
            new_loc = (location.in_direction(new_dir), new_dir)
            if new_loc not in seen:
                to_check.add(new_loc)
    return len(energized)


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    mirror_grid = MirrorGrid()
    for line_idx, line in enumerate(input_file.read_text().splitlines()):
        mirror_grid.size = len(line)
        for col_idx, char in enumerate(line):
            if char != ".":
                mirror_grid.grid[Coord(col_idx, mirror_grid.size - 1 - line_idx)] = char

    p1 = light_beam(Coord(0, mirror_grid.size - 1), Direction.EAST, mirror_grid)

    poss = []
    for x in range(mirror_grid.size):
        poss.append(light_beam(Coord(0, x), Direction.EAST, mirror_grid))
    for x in range(mirror_grid.size):
        poss.append(light_beam(Coord(x, 0), Direction.NORTH, mirror_grid))
    for x in range(mirror_grid.size):
        poss.append(
            light_beam(Coord(mirror_grid.size - 1, x), Direction.WEST, mirror_grid)
        )
    for x in range(mirror_grid.size):
        poss.append(
            light_beam(Coord(x, mirror_grid.size - 1), Direction.SOUTH, mirror_grid)
        )

    return (p1, max(poss))


if __name__ == "__main__":
    utils.per_day_main(p1p2, "")
