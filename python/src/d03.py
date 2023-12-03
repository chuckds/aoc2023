"""
Advent Of Code 2023 Day 03
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable, NamedTuple

import utils


class Coord(NamedTuple):
    line: int
    col: int

    def adjacent_coord(self) -> Iterable[Coord]:
        for line_delta in (-1, 0, 1):
            for col_delta in (-1, 0, 1):
                yield Coord(self.line + line_delta, self.col + col_delta)


def parse_input(
    lines: list[str],
) -> tuple[list[tuple[int, set[Coord]]], set[Coord], set[Coord]]:
    numbers = []
    symbols = set()
    poss_gears = set()
    for line_num, line in enumerate(lines):
        num = ""
        adjacent_coords: set[Coord] = set()
        for col_num, char in enumerate(line):
            current_coord = Coord(line_num, col_num)
            if char.isdigit():
                num += char
                adjacent_coords.update(c for c in current_coord.adjacent_coord())
            else:
                if num:
                    numbers.append((int(num), adjacent_coords))
                    num = ""
                    adjacent_coords = set()
                if char != ".":
                    symbols.add(current_coord)
                    if char == "*":
                        poss_gears.add(current_coord)
        if num:
            numbers.append((int(num), adjacent_coords))
    return numbers, symbols, poss_gears


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    numbers, symbols, poss_gears = parse_input(input_file.read_text().splitlines())

    part_numbers = [
        num for num, adjacent_coords in numbers if adjacent_coords & symbols
    ]
    gear_ratios = []
    for gear_coord in poss_gears:
        adjacent_nums = [
            num for num, adjacent_coords in numbers if gear_coord in adjacent_coords
        ]
        if len(adjacent_nums) == 2:
            gear_ratios.append(math.prod(adjacent_nums))

    return (sum(part_numbers), sum(gear_ratios))


if __name__ == "__main__":
    utils.per_day_main(p1p2)
