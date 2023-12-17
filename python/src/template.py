"""
Advent Of Code 2023 Day XXX
"""

from __future__ import annotations

from pathlib import Path

import utils


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    for line in input_file.read_text().splitlines():
        pass
    return (None, None)


if __name__ == "__main__":
    utils.per_day_main(p1p2)
