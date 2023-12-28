"""
Advent Of Code 2023 Day 17
"""

from __future__ import annotations

import enum
import heapq
from functools import total_ordering
from pathlib import Path
from typing import NamedTuple

import utils


@total_ordering
class Direction(enum.Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    WEST = (-1, 0)
    EAST = (1, 0)

    def __lt__(self, other: Direction) -> bool:
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


DIR_TO_ORTHOG = {
    dir: (
        Direction((-1 * dir.value[1], dir.value[0])),
        Direction((dir.value[1], -1 * dir.value[0])),
    )
    for dir in Direction
}


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
    city_blocks: dict[Coord, CityBlock] = {
        (location := Coord(col_idx, line_idx)): CityBlock(location, heat_loss, {})
        for line_idx, line in enumerate(grid)
        for col_idx, heat_loss in enumerate(line)
    }

    for location, city_block in city_blocks.items():
        for in_dir in Direction:
            new_loc = location.in_direction(in_dir)
            adj = city_blocks.get(new_loc)
            if adj:
                city_block.connected[in_dir] = adj

    return city_blocks


def min_heat_loss(start: CityBlock, end: CityBlock, p2: bool) -> int:
    to_check: list[tuple[int, tuple[CityBlock, Direction]]] = [
        (0, (start, a_dir)) for a_dir in (Direction.SOUTH, Direction.EAST)
    ]
    heapq.heapify(to_check)
    visited = set()
    while to_check:
        heat_loss, walk_state = heapq.heappop(to_check)
        if walk_state in visited:
            continue
        visited.add(walk_state)
        block, prev_dir = walk_state
        if block is end:
            break
        for new_dir in DIR_TO_ORTHOG[prev_dir]:
            new_heat_loss, new_block = heat_loss, block
            for num_straight in range(10 if p2 else 3):
                if not (new_block := new_block.connected.get(new_dir)):  # type: ignore[assignment]
                    break  # Heading in this direction is out of bounds
                new_heat_loss += new_block.heat_loss
                if not p2 or new_block == end or num_straight >= 3:
                    walk_state = (new_block, new_dir)
                    if walk_state in visited:
                        continue
                    heapq.heappush(to_check, (new_heat_loss, walk_state))
    return heat_loss


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, ...]:
    grid = [
        [int(char) for char in line] for line in input_file.read_text().splitlines()
    ]
    city_blocks = construct_city(grid)
    return tuple(
        min_heat_loss(
            city_blocks[Coord(0, 0)],
            city_blocks[Coord(len(grid[0]) - 1, len(grid[0]) - 1)],
            is_p2,
        )
        for is_p2 in (False, True)
    )


if __name__ == "__main__":
    utils.per_day_main(p1p2, "")
