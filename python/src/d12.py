"""
Advent Of Code 2023 Day 12
"""

from __future__ import annotations

import itertools
from pathlib import Path
from typing import Iterable, NamedTuple

import utils


class SpringLine(NamedTuple):
    rep_list: list[str]
    damaged_groups: list[int]
    unknown_idxs: set[int]
    broken_idxs: set[int]

    @classmethod
    def from_spring_groups(cls, springs: str, groups: str) -> SpringLine:
        return cls(
            ["#" if char == "#" else " " for char in springs],
            [int(size) for size in groups.split(",")],
            {idx for idx, char in enumerate(springs) if char == "?"},
            {idx for idx, char in enumerate(springs) if char == "#"},
        )

    @classmethod
    def from_line(cls, line: str) -> SpringLine:
        return cls.from_spring_groups(*line.split())

    @classmethod
    def from_p2_line(cls, line: str) -> SpringLine:
        springs, groups = line.split()
        return cls.from_spring_groups("?".join([springs] * 5), ",".join([groups] * 5))

    def is_valid(self, new_broken_idxs: Iterable[int]) -> bool:
        def reset() -> None:
            for idx in new_broken_idxs:
                self.rep_list[idx] = " "
        for idx in new_broken_idxs:
            self.rep_list[idx] = "#"
        broken_groups = "".join(self.rep_list).split()
        if len(broken_groups) != len(self.damaged_groups):
            reset()
            return False
        res = all(exp_size == len(group) for exp_size, group in zip(self.damaged_groups, broken_groups))
        reset()
        return res


def get_num_arrangements(spring_rows: list[SpringLine]) -> int:
    valid_options = 0
    for idx, spring_row in enumerate(spring_rows):
        missing_broken = sum(spring_row.damaged_groups) - len(spring_row.broken_idxs)
        valid_options += sum(
            1 for new_broken_idxs in itertools.combinations(spring_row.unknown_idxs, missing_broken)
            if spring_row.is_valid(new_broken_idxs)
        )
        print(f"{idx} done line")
    return valid_options


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    spring_rows = [
        SpringLine.from_line(line) for line in input_file.read_text().splitlines()
    ]
    p1 = get_num_arrangements(spring_rows)
    spring_rowsp2 = [
        SpringLine.from_p2_line(line) for line in input_file.read_text().splitlines()
    ]
    print(len(spring_rowsp2))
    #p2 = get_num_arrangements(spring_rowsp2)
    p2 = 0
    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main(p1p2, example_only=True)
