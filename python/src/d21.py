"""
Advent Of Code 2023 Day 21
"""

from __future__ import annotations

import enum
from pathlib import Path
from typing import Generator, NamedTuple

import utils


class Direction(enum.Enum):
    NORTH = (0, 1)
    SOUTH = (0, -1)
    WEST = (-1, 0)
    EAST = (1, 0)


class Coord(NamedTuple):
    col: int
    line: int

    def in_direction(self, direction: Direction) -> Coord:
        return Coord(self.col + direction.value[0], self.line + direction.value[1])

    def adjacent(self) -> Generator[Coord, None, None]:
        for a_dir in Direction:
            yield self.in_direction(a_dir)


def grid_coord(a_point: Coord, size: int) -> Coord:
    return Coord(a_point.col // size, a_point.line // size)


def get_infini_reachable(
    gardens: set[Coord], start: Coord, num_steps: tuple[int, ...], size: int
) -> list[int]:
    step_from = set([start])
    reachable = {Coord(0, 0): {0: set([start])}}
    answers = []
    for step in range(max(num_steps)):
        new_step_starts = set()
        for loc in step_from:
            for new_loc in loc.adjacent():
                mod_grid_loc = Coord(new_loc.col % size, new_loc.line % size)
                if mod_grid_loc in gardens and new_loc not in reachable.setdefault(
                    grid := grid_coord(new_loc, size), {}
                ).setdefault((step + 1) % 2, set()):
                    new_step_starts.add(new_loc)
                    reachable[grid][(step + 1) % 2].add(mod_grid_loc)
                    # if reachable[grid] == max_reachable:
                    #    complete_grids.add(grid)
        if (step + 1) in num_steps:
            answers.append(
                sum(
                    len(grid_reach[(step + 1) % 2]) for grid_reach in reachable.values()
                )
            )
        step_from = new_step_starts
    # grids_like_start = [abs(grid.col) + abs(grid.line) for grid in complete_grids if reachable[grid][0] == reachable[Coord(0, 0)][0]]
    # grids_start_flip = [abs(grid.col) + abs(grid.line) for grid in complete_grids if reachable[grid][1] == reachable[Coord(0, 0)][0]]
    return answers


def get_max_reachable(
    gardens: set[Coord], start: Coord
) -> tuple[dict[int, dict[Coord, int]], int]:
    step_from = set([start])
    reachable: dict[int, dict[Coord, int]] = {0: {start: 0}, 1: {}}
    step = 0
    while step_from:
        new_step_starts = set()
        for loc in step_from:
            for new_loc in loc.adjacent():
                if new_loc in gardens and new_loc not in reachable[(step + 1) % 2]:
                    new_step_starts.add(new_loc)
                    reachable[(step + 1) % 2][new_loc] = step + 1
        step_from = new_step_starts
        step += 1
    return reachable, step


def get_reachable(gardens: set[Coord], start: Coord, num_steps: int) -> int:
    step_from = set([start])
    reachable: dict[int, set[Coord]] = {0: set([start]), 1: set()}
    for step in range(num_steps):
        new_step_starts = set()
        for loc in step_from:
            for new_loc in loc.adjacent():
                if new_loc in gardens and new_loc not in reachable[(step + 1) % 2]:
                    new_step_starts.add(new_loc)
                    reachable[(step + 1) % 2].add(new_loc)
        step_from = new_step_starts
    return len(reachable[num_steps % 2])


def parse_garden(lines: list[str]) -> tuple[Coord, set[Coord], int]:
    starts = []

    def start_char(col: int, line: int) -> Coord:
        starts.append(Coord(col, line))
        return starts[0]

    gardens = {
        Coord(col_idx, line_idx) if char != "S" else start_char(col_idx, line_idx)
        for line_idx, line in enumerate(lines)
        for col_idx, char in enumerate(line)
        if char != "#"
    }
    return starts[0], gardens, len(lines)


def p1p2(
    input_file: Path = utils.real_input(),
) -> tuple[int | None, tuple[int, ...] | None]:
    is_example = "example" in str(input_file)
    start, gardens, size = parse_garden(input_file.read_text().splitlines())

    max_reachable, steps_required = get_max_reachable(gardens, start)
    if is_example:
        p2s = tuple(
            get_infini_reachable(gardens, start, (6, 10, 50), size)
            # get_infini_reachable(gardens, start, (6, 10, 50, 100, 500, 1000, 5000), size)
        )
    else:
        p2s = tuple(get_infini_reachable(gardens, start, (200,), size))
        # p2s = tuple(get_infini_reachable(gardens, start, (26501365,), size))
    return (get_reachable(gardens, start, 6 if is_example else 64), p2s)


if __name__ == "__main__":
    utils.per_day_main(p1p2, "example")
