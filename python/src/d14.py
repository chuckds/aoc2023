"""
Advent Of Code 2023 Day 14
"""

from __future__ import annotations

import enum
from pathlib import Path
from typing import Iterable, NamedTuple

import utils

p2_cycles = 1_000_000_000


class Direction(enum.Enum):
    NORTH = (0, 1)
    WEST = (-1, 0)
    SOUTH = (0, -1)
    EAST = (1, 0)

    def opposite(self) -> Direction:
        return Direction((self.value[0] * -1, self.value[1] * -1))


class Coord(NamedTuple):
    col: int
    line: int

    def in_dir(self, a_dir: Direction) -> Coord:
        return Coord(self[0] + a_dir.value[0], self[1] + a_dir.value[1])


def get_north_load(rounds: Iterable[Coord]) -> int:
    return sum(1 + round[1] for round in rounds)


def tilt(
    tilt_dir: Direction, size: int, rounds: set[Coord], squares: set[Coord]
) -> set[Coord]:
    move_dir = tilt_dir.opposite()
    new_rounds = set()
    for dim_idx in range(size):
        if tilt_dir.value[0] == 0:  # North or South
            coord = rest = Coord(dim_idx, size - 1 if tilt_dir.value[1] == 1 else 0)
        else:
            coord = rest = Coord(size - 1 if tilt_dir.value[0] == 1 else 0, dim_idx)  # type: ignore[comparison-overlap]
        for _ in range(size):
            next_coord = coord.in_dir(move_dir)
            if coord in squares:
                rest = next_coord
            elif coord in rounds:
                new_rounds.add(rest)
                rest = rest.in_dir(move_dir)
            coord = next_coord
    return new_rounds


def parse(input_file: Path) -> tuple[dict[str, set[Coord]], int]:
    rocks: dict[str, set[Coord]] = {"O": set(), "#": set()}
    for line_idx, line in enumerate(input_file.read_text().splitlines()):
        size = len(line)
        for col_idx, char in enumerate(line):
            if char in rocks:
                rocks[char].add(Coord(col_idx, size - line_idx - 1))
    return rocks, size


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    rocks, size = parse(input_file)
    rounds_after_tilt = tilt(Direction.NORTH, size, rocks["O"], rocks["#"])

    rounds = rocks["O"]
    f_rounds = frozenset(rounds)
    seen_configs: dict[frozenset[Coord], int] = {}
    while (loop_rejoin := seen_configs.get(f_rounds, None)) is None:
        seen_configs[f_rounds] = len(seen_configs)
        for a_dir in Direction:
            rounds = tilt(a_dir, size, rounds, rocks["#"])
        f_rounds = frozenset(rounds)

    loop_len = len(seen_configs) - loop_rejoin
    part_loop = (p2_cycles - loop_rejoin) % loop_len
    final_config = next(
        rounds for rounds, idx in seen_configs.items() if idx == part_loop + loop_rejoin
    )

    return (get_north_load(rounds_after_tilt), get_north_load(final_config))


if __name__ == "__main__":
    utils.per_day_main(p1p2)
