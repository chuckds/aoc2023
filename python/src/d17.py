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


DIR_TO_OPPOSITE = {dir: Direction((dir.value[0] * -1, dir.value[1] * -1))
                   for dir in Direction}


class Coord(NamedTuple):
    col: int
    line: int

    def in_direction(self, direction: Direction) -> Coord:
        return Coord(self.col + direction.value[0], self.line + direction.value[1])


class CityBlock(NamedTuple):
    location: Coord
    heat_loss: int
    connected: dict[Direction, CityBlock]

    def __hash__(self) -> int:
        return hash(self.location)


def construct_city(grid: list[list[int]]) -> dict[Coord, CityBlock]:
    city_blocks: dict[Coord, CityBlock] = {}
    for line_idx, line in enumerate(grid):
        for col_idx, heat_loss in enumerate(line):
            location = Coord(col_idx, line_idx)
            city_blocks[location] = CityBlock(location, heat_loss, {})

    for location, city_block in city_blocks.items():
        for in_dir in Direction:
            new_loc = location.in_direction(in_dir)
            adj = city_blocks.get(new_loc)
            if adj:
                city_block.connected[in_dir] = adj

    return city_blocks


def min_heat_loss_cb(start: CityBlock, end: CityBlock, p2: bool) -> int:
    to_check: list[tuple[int, tuple[CityBlock, int, Direction]]] = [
        (0, (start, 0, Direction.SOUTH)),
        (0, (start, 0, Direction.EAST))
    ]
    visited = set()
    while to_check:
        heat_loss, walk_state = to_check.pop()
        if walk_state in visited:
            continue
        visited.add(walk_state)
        block, num_straights, prev_dir = walk_state
        if block == end:
            return -1 * heat_loss
        from_dir = DIR_TO_OPPOSITE[prev_dir]
        for new_dir, new_block in block.connected.items():
            if new_dir == from_dir:  # Can't go backwards
                continue
            if new_dir == prev_dir:  # Straight on
                if num_straights >= (10 if p2 else 3):
                    continue
            elif p2 and num_straights <= 3:
                continue
            walk_state = (
                new_block,
                num_straights + 1 if new_dir == prev_dir else 1,
                new_dir
            )
            if walk_state in visited:
                continue
            bisect.insort(
                to_check,
                (heat_loss - new_block.heat_loss, walk_state),
                key=lambda x: x[0],
            )
    return 0


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, ...]:
    grid = [
        [int(char) for char in line]
        for line in input_file.read_text().splitlines()
    ]

    city_blocks = construct_city(grid)
    return tuple(
        min_heat_loss_cb(city_blocks[Coord(0, 0)],
                         city_blocks[Coord(len(grid[0]) - 1, len(grid[0]) - 1)],
                         is_p2)
        for is_p2 in (False, True)
    )


if __name__ == "__main__":
    utils.per_day_main(p1p2)
