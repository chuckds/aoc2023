"""
Advent Of Code 2023 Day XXX
"""

from __future__ import annotations

from pathlib import Path

import utils


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p1, p2 = (0, 0)
    for line in input_file.read_text().splitlines():
        pass
    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main()
