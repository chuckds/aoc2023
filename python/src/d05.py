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


def get_mapped_range(
    seed_range: range, map_range: MapRange
) -> tuple[list[range], range | None]:
    if (
        seed_range.start >= map_range.source.stop
        or seed_range.stop <= map_range.source.start
    ):  # disjoint
        return ([seed_range], None)
    else:
        unmapped = []
        if seed_range.start < map_range.source.start:
            # Part of the range doesn't overlap
            unmapped.append(range(seed_range.start, map_range.source.start))
        mapped_start = max(seed_range.start, map_range.source.start)
        mapped_len = min(seed_range.stop, map_range.source.stop) - mapped_start
        new_start = map_range.dest_st + map_range.source.index(mapped_start)
        mapped = range(new_start, new_start + mapped_len)
        if seed_range.stop > map_range.source.stop:
            # Unmapped the other side
            unmapped.append(range(map_range.source.stop, seed_range.stop))
        return (unmapped, mapped)


def location_from_seed_range(seed_range: range, mappings: list[list[MapRange]]) -> int:
    seed_ranges = [seed_range]
    for ranges in mappings:
        mapped_ranges = []
        for source_range in ranges:
            unmapped_ranges = []
            for seed_range in seed_ranges:
                new_unmapped_ranges, new_mapped_ranges = get_mapped_range(
                    seed_range, source_range
                )
                unmapped_ranges.extend(new_unmapped_ranges)
                if new_mapped_ranges is not None:
                    mapped_ranges.append(new_mapped_ranges)
            seed_ranges = unmapped_ranges
        seed_ranges = unmapped_ranges + mapped_ranges
    return min(seed_range.start for seed_range in seed_ranges)


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
    seed_ranges = (
        range(seed_st, seed_st + length)
        for seed_st, length in zip(seeds[::2], seeds[1::2])
    )
    return (
        p1,
        min(
            location_from_seed_range(seed_range, mappings) for seed_range in seed_ranges
        ),
    )


if __name__ == "__main__":
    utils.per_day_main(p1p2, example_only=False)
