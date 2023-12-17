"""
Advent Of Code 2023 Day 15
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import utils


def hash(input: str) -> int:
    val = 0
    for char in input:
        val += ord(char)
        val *= 17
        val %= 256
    return val


class Lens(NamedTuple):
    label: str
    in_box: int
    at_step: int
    focal_length: int


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    steps = input_file.read_text().splitlines()[0].split(",")
    hashes = (hash(step) for step in steps)

    box_to_labels: dict[int, dict[str, Lens]] = {}
    for step_idx, step in enumerate(steps):
        if step[-1] == "-":
            label = step[:-1]
            box_num = hash(label)
            box_to_labels.get(box_num, {}).pop(label, None)
        else:
            label, focal_str = step.split("=")
            focal_length = int(focal_str)
            box_num = hash(label)
            old_lens = box_to_labels.get(box_num, {}).get(label)
            if old_lens is None:
                box_to_labels.setdefault(box_num, {})[label] = Lens(label, box_num, step_idx, focal_length)
            else:
                box_to_labels[box_num][label] = Lens(label, box_num, old_lens.at_step, focal_length)

    focussing_power = (
        (1 + box_num) * lens.focal_length * (lens_idx + 1)
        for box_num, lenses in box_to_labels.items()
        for lens_idx, lens in enumerate(sorted(lenses.values(), key=lambda lens: lens.at_step))
    )

    return (sum(hashes), sum(focussing_power))


if __name__ == "__main__":
    utils.per_day_main(p1p2)
