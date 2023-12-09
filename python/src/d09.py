"""
Advent Of Code 2023 Day 9
"""

from __future__ import annotations

from pathlib import Path

import utils


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    value_histories = (
        [int(token) for token in line.split()]
        for line in input_file.read_text().splitlines()
    )
    next_vals = []
    prev_vals = []
    for value_history in value_histories:
        first_differnces = [value_history[0]]
        next_val = value_history[-1]
        while any(value_history):
            value_history = [
                next - prev
                for next, prev in zip(value_history[1:], value_history)
            ]
            next_val += value_history[-1]
            first_differnces.append(value_history[0])
        next_vals.append(next_val)
        first_val = 0
        for diff in first_differnces[::-1]:
            first_val = diff - first_val
        prev_vals.append(first_val)

    return (sum(next_vals), sum(prev_vals))


if __name__ == "__main__":
    utils.per_day_main(p1p2, example_only=False)
