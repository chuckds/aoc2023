"""
Advent Of Code 2023 Day 03
"""

from __future__ import annotations

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


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p2 = 0
    numbers = []
    symbols = set()
    for line_num, line in enumerate(input_file.read_text().splitlines()):
        num = ""
        adjacent_coords: set[Coord] = set()
        for col_num, char in enumerate(line):
            if char.isdigit():
                num += char
                adjacent_coords.update(
                    c for c in Coord(line_num, col_num).adjacent_coord()
                )
            else:
                if num:
                    numbers.append((int(num), adjacent_coords))
                    num = ""
                    adjacent_coords = set()
                if char != ".":
                    symbols.add(Coord(line_num, col_num))
        if num:
            numbers.append((int(num), adjacent_coords))

    part_numbers = [
        num for num, adjacent_coords in numbers if adjacent_coords & symbols
    ]

    return (sum(part_numbers), p2)


if __name__ == "__main__":
    utils.per_day_main(p1p2)
