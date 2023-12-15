"""
Advent Of Code 2023 Day 14
"""

from __future__ import annotations

from pathlib import Path

import utils


p2_cycles = 1_000_000_000


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    cols: dict[int, list[tuple[int, str]]] = {}
    for line_idx, line in enumerate(input_file.read_text().splitlines()):
        for col_idx, char in enumerate(line):
            if char != ".":
                cols.setdefault(col_idx, []).append((line_idx, char))
    col_depth = line_idx + 1
    t_score = 0
    for col in cols.values():
        col_score = rest_idx = 0
        for line_idx, char in col:
            if char == "#":
                rest_idx = line_idx + 1
            else:
                col_score += col_depth - rest_idx
                rest_idx += 1
        t_score += col_score
    return (t_score, None)


if __name__ == "__main__":
    utils.per_day_main(p1p2, example_only=False)
