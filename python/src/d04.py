"""
Advent Of Code 2023 Day 04
"""

from __future__ import annotations

from pathlib import Path

import utils


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    cards = (
        [
            {int(num_str) for num_str in num_list.split()}
            for num_list in line.split(":")[1].split("|")
        ]
        for line in input_file.read_text().splitlines()
    )

    matching_numbers = [len(winning_num & got_nums) for winning_num, got_nums in cards]
    scores = (
        2 ** (num_matching - 1) if num_matching else 0
        for num_matching in matching_numbers
    )

    num_of_each = [1] * len(matching_numbers)
    for idx, matching_nums in enumerate(matching_numbers):
        for jdx in range(idx + 1, idx + 1 + matching_nums):
            num_of_each[jdx] += num_of_each[idx]

    return (sum(scores), sum(num_of_each))


if __name__ == "__main__":
    utils.per_day_main(p1p2)
