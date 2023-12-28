"""
Advent Of Code 2023 Day 12
"""

from __future__ import annotations

from functools import cache
from pathlib import Path
from typing import NamedTuple, Sequence

import utils


def consume_groups(
    line: str, num_damaged_to_add: int, exp_dam_groups: Sequence[int]
) -> tuple[int, int, int] | None:
    """No ? in line"""
    group_len_idx = 0
    next_dam_group_len = exp_dam_groups[group_len_idx] if exp_dam_groups else -1
    curr_dam_group_len = 0
    for idx, char in enumerate(line):
        if char == "?":
            if curr_dam_group_len:
                # We're part way through a damage group
                if curr_dam_group_len == next_dam_group_len:  # Assume gap
                    char = "."
                elif num_damaged_to_add:  # Assume broken
                    char = "#"
                    num_damaged_to_add -= 1
                else:  # This unknown can't be broken, and if it was a gap the groups wouldn't match
                    return None
            else:  # Could be either
                return idx, num_damaged_to_add, group_len_idx

        if char == "#":
            if curr_dam_group_len < next_dam_group_len:
                curr_dam_group_len += 1
            else:  # Run of brokens is too long, no match
                return None
        else:  # char is a gap
            if curr_dam_group_len:  # End of a group
                if curr_dam_group_len == next_dam_group_len:
                    group_len_idx += 1
                    next_dam_group_len = (
                        exp_dam_groups[group_len_idx]
                        if group_len_idx < len(exp_dam_groups)
                        else -1
                    )
                    curr_dam_group_len = 0
                else:  # Run of brokens is too short, doesn't match
                    return None

    if curr_dam_group_len:  # Finished in a group of brokens
        if curr_dam_group_len == next_dam_group_len:  # Which was the right size
            group_len_idx += 1
        else:
            return None
    return -1, num_damaged_to_add, group_len_idx


@cache
def spring_line_variations(
    line: str, num_damaged_to_add: int, exp_dam_groups: Sequence[int]
) -> int:
    consume_res = consume_groups(line, num_damaged_to_add, exp_dam_groups)
    if consume_res:
        idx_at, num_damaged_to_add, groups_consumed = consume_res
        if idx_at >= 0:
            # Hit a "?" that could be either
            line_left = line[idx_at + 1 :]
            min_required_len = (
                num_damaged_to_add + len(exp_dam_groups) - groups_consumed - 1
            )
            if min_required_len <= len(line_left):
                as_gap = spring_line_variations(
                    line_left, num_damaged_to_add, exp_dam_groups[groups_consumed:]
                )
            else:
                as_gap = 0
            as_broken = spring_line_variations(
                "#" + line_left,
                num_damaged_to_add - 1,
                exp_dam_groups[groups_consumed:],
            )
            return as_gap + as_broken
        else:
            if num_damaged_to_add == 0:  # All good!
                return 1
            return 0
    else:  # Not viable
        return 0


class SpringLine(NamedTuple):
    line: str
    damaged_groups: Sequence[int]

    @classmethod
    def from_spring_groups(cls, springs: str, groups: str) -> SpringLine:
        return cls(springs, tuple(int(size) for size in groups.split(",")))

    @classmethod
    def from_p2_line(cls, line: str) -> SpringLine:
        springs, groups = line.split()
        return cls.from_spring_groups("?".join([springs] * 5), ",".join([groups] * 5))

    def get_num_arrangements(self) -> int:
        return spring_line_variations(
            self.line,
            sum(self.damaged_groups) - sum(1 for char in self.line if char == "#"),
            self.damaged_groups,
        )


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    spring_rows = (
        SpringLine.from_spring_groups(*line.split())
        for line in input_file.read_text().splitlines()
    )
    spring_rows2 = (
        SpringLine.from_p2_line(line) for line in input_file.read_text().splitlines()
    )
    return (
        sum(spring_row.get_num_arrangements() for spring_row in spring_rows),
        sum(spring_row.get_num_arrangements() for spring_row in spring_rows2),
    )


if __name__ == "__main__":
    utils.per_day_main(p1p2)
