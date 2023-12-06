"""
Advent Of Code 2023 Day 06
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Generator

import utils


def get_ways_to_win(time: int, max_distance: int) -> int:
    """
    Get the number of ways to win.

    Distance = time Holding button x (Max time - time Holding buttin)
    d = h x (M - h)
    d = Mh - h ^ 2

    To find h (time holding button) for a given distance:
    0 = -h^2 + Mh - d
    Crack open GCSE maths
    h = (M +/- srqt(M^2 - 4d)) / 2

    """
    tricky_bit = math.sqrt(time**2 - 4 * max_distance)
    vals = ((time + sign * tricky_bit) / 2 for sign in (-1, 1))
    # Now do annoying rounding stuff
    int_vals = [
        int(val) + sign if int(val) == val else math.ceil(val)
        for val, sign in zip(vals, (1, 0))
    ]
    return int_vals[1] - int_vals[0]


def get_nums(line: str) -> tuple[Generator[int, None, None], int]:
    str_nums = line.split(":")[1].split()
    return (int(token) for token in str_nums), int("".join(str_nums))


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    lines = input_file.read_text().splitlines()
    times, p2_time = get_nums(lines[0])
    distances, p2_dist = get_nums(lines[1])

    ways_to_win = (
        get_ways_to_win(time, max_distance)
        for time, max_distance in zip(times, distances)
    )
    return (math.prod(ways_to_win), get_ways_to_win(p2_time, p2_dist))


if __name__ == "__main__":
    utils.per_day_main(p1p2, example_only=False)
