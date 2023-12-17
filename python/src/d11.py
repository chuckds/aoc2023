"""
Advent Of Code 2023 Day 11
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
from typing import NamedTuple

import utils


class Coord(NamedTuple):
    col: int
    line: int

    def distance_between(self, other: Coord) -> int:
        return abs(self.col - other.col) + abs(self.line - other.line)


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    galaxies: list[Coord] = []
    for line_num, line in enumerate(input_file.read_text().splitlines()):
        galaxies.extend(
            (
                Coord(col_num, line_num)
                for col_num in (
                    col_num for col_num, char in enumerate(line) if char == "#"
                )
            )
        )
    empty_cols = set(range(len(line) + 1)) - set(gal.col for gal in galaxies)
    empty_lines = set(range(line_num + 1)) - set(gal.line for gal in galaxies)

    total_sep = empty_dim = 0
    for a_gal, b_gal in combinations(galaxies, 2):
        total_sep += a_gal.distance_between(b_gal)
        l_range = range(min(a_gal.line, b_gal.line), max(a_gal.line, b_gal.line))
        c_range = range(min(a_gal.col, b_gal.col), max(a_gal.col, b_gal.col))
        empty_dim += sum(1 for li in empty_lines if li in l_range)
        empty_dim += sum(1 for co in empty_cols if co in c_range)
    empty_multi = (100 if "example" in str(input_file) else 1000000) - 1
    return (total_sep + empty_dim, total_sep + empty_multi * empty_dim)


if __name__ == "__main__":
    utils.per_day_main(p1p2)
