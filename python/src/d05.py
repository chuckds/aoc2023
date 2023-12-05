"""
Advent Of Code 2023 Day 05
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import utils


class MapRange(NamedTuple):
    source: range
    dest_st: int


def location_from_seed(seed: int, mappings: list[list[MapRange]]) -> int:
    for ranges in mappings:
        for source_range in ranges:
            try:
                index = source_range.source.index(seed)
                seed = source_range.dest_st + index
                break
            except ValueError:  # seed not in range
                pass
    return seed


def parse(lines: list[str]) -> list[list[MapRange]]:
    mappings: list[list[MapRange]] = []
    ranges = []
    for line in lines:
        if not line:
            continue
        if line[0].isdigit():
            dest_st, source_st, length = (int(token) for token in line.split())
            ranges.append(MapRange(range(source_st, source_st + length), dest_st))
        elif ranges:
            mappings.append(ranges)
            ranges = []

    if ranges:
        mappings.append(ranges)
    return mappings


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    lines = input_file.read_text().splitlines()
    seeds = [int(token) for token in lines.pop(0).split(":")[1].split()]
    mappings = parse(lines)

    p1 = min(location_from_seed(seed, mappings) for seed in seeds)
    seed_ranges = [range(seed_st, seed_st + length) for seed_st, length in zip(seeds[::2], seeds[1::2])]
    p2_seeds = {seed for seed_range in seed_ranges for seed in seed_range}
    return (p1, min(location_from_seed(seed, mappings) for seed in p2_seeds))


if __name__ == "__main__":
    utils.per_day_main(p1p2)
