"""
Advent Of Code 2023 Day 02
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import NamedTuple

import utils


class GameBallCounts(NamedTuple):
    red: int = 0
    green: int = 0
    blue: int = 0

    def is_possible(self, limit: GameBallCounts) -> bool:
        return all(bc <= lc for bc, lc in zip(self, limit))


def get_game_ball_counts(ball_counts: str) -> list[GameBallCounts]:
    gbcs = []
    for cube_reveals in ball_counts.split(";"):
        colour_counts = {}
        for colour_count_str in cube_reveals.split(","):
            count, colour = colour_count_str.strip().split()
            colour_counts[colour] = int(count)
        gbcs.append(GameBallCounts(**colour_counts))
    return gbcs


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    games = [
        get_game_ball_counts(line.split(":")[1].strip())
        for line in input_file.read_text().splitlines()
    ]

    p1_limit = GameBallCounts(12, 13, 14)
    valid_games = [
        idx + 1
        for idx, game_reveals in enumerate(games)
        if all(game_reveal.is_possible(p1_limit) for game_reveal in game_reveals)
    ]
    min_colours = [
        GameBallCounts(
            *(
                max(gr[idx] for gr in game_reveals)
                for idx in range(len(GameBallCounts._fields))
            )
        )
        for game_reveals in games
    ]
    return (sum(valid_games), sum(math.prod(gbc) for gbc in min_colours))


if __name__ == "__main__":
    utils.per_day_main(p1p2)
