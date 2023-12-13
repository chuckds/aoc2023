"""
Advent Of Code 2023 Day 13
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import utils


@dataclass
class Pattern:
    rows: list[str] = field(default_factory=list)
    cols: list[str] = field(default_factory=list)


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    patterns: list[Pattern] = []
    pattern = Pattern()
    for line in input_file.read_text().splitlines():
        if line:
            pattern.rows.append(line)
        else:
            patterns.append(pattern)
            pattern = Pattern()
    patterns.append(pattern)

    for pattern in patterns:
        for idx in range(len(pattern.rows[0])):
            pattern.cols.append("".join(row[idx] for row in pattern.rows))

    p1 = p2 = 0
    for pattern in patterns:
        for dim, factor in ((pattern.rows, 100), (pattern.cols, 1)):
            for mirror_idx in range(1, len(dim)):
                diffs = [(b4_idx, after_idx) for (b4_idx, b4), (after_idx, after) in
                       zip(
                           ((idx, dim[idx]) for idx in range(mirror_idx - 1, -1, -1)),
                           ((idx, dim[idx]) for idx in range(mirror_idx, len(dim)))
                       ) if b4 != after
                ]
                if len(diffs) == 0:  # Found the reflection
                    p1 += mirror_idx * factor
                elif len(diffs) == 1:
                    # Only one row/column doesn't match check if only one char
                    # is wrong - if so it is the smudge
                    chars_diff = sum(1 for b4_char, after_char
                                     in zip(dim[diffs[0][0]], dim[diffs[0][1]])
                                     if b4_char != after_char)
                    if chars_diff == 1:
                        p2 += mirror_idx * factor

    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main(p1p2, example_only=False)
