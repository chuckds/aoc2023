"""
Advent Of Code 2023 Day 07
"""

from __future__ import annotations

import enum
from collections import Counter
from pathlib import Path
from typing import NamedTuple

import utils


CARD_ORDER = "AKQJT98765432"
CARD_TO_ORDER = {card: idx for idx, card in enumerate(CARD_ORDER[::-1])}
CARD_TO_ORDER_P2 = {card: idx for idx, card in enumerate((CARD_ORDER.replace("J","") + "J")[::-1])}


class HandType(enum.IntEnum):
    HIGH_CARD = enum.auto()
    ONE_PAIR = enum.auto()
    TWO_PAIR = enum.auto()
    THREE_KIND = enum.auto()
    FULL_HOUSE = enum.auto()
    FOUR_KIND = enum.auto()
    FIVE_KIND = enum.auto()


class HandRank(NamedTuple):
    rank: int
    value: int


def get_hand_type(num_groups: int, size_longest_group: int) -> HandType:
    match num_groups:
        case 1:
            return HandType.FIVE_KIND
        case 2:
            return HandType.FOUR_KIND if size_longest_group == 4 else HandType.FULL_HOUSE
        case 3:
            return HandType.THREE_KIND if size_longest_group == 3 else HandType.TWO_PAIR
        case 4:
            return HandType.ONE_PAIR
        case _:  # 5
            return HandType.HIGH_CARD


def hand_to_val(hand: str, order: dict[str, int]) -> int:
    return sum(order[card] * 13**exponent for exponent, card in enumerate(hand[::-1]))


def get_hand_ranks(hand: str) -> tuple[HandRank, HandRank]:
    card_count = Counter(hand)
    most_common_2 = card_count.most_common(2)
    p1 = get_hand_type(len(card_count), most_common_2[0][1])
    num_js = card_count["J"]
    if 0 < num_js < 5:
        size_of_group_to_join = most_common_2[1][1] if most_common_2[0][0] == "J" else most_common_2[0][1]
        p2 = get_hand_type(len(card_count) - 1, num_js + size_of_group_to_join)
    else:
        p2 = p1
    return (HandRank(p1, hand_to_val(hand, CARD_TO_ORDER)),
            HandRank(p2, hand_to_val(hand, CARD_TO_ORDER_P2)))


class Hand(NamedTuple):
    bid: int
    p1_rank: HandRank
    p2_rank: HandRank

    @classmethod
    def from_line(cls, line: str) -> Hand:
        tokens = line.split()
        return cls(int(tokens[1]), *get_hand_ranks(tokens[0]))


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    hands = [Hand.from_line(line) for line in input_file.read_text().splitlines()]

    p1 = sum((idx + 1) * hand.bid for idx, hand in enumerate(sorted(hands, key=lambda hand: hand.p1_rank)))
    p2 = sum((idx + 1) * hand.bid for idx, hand in enumerate(sorted(hands, key=lambda hand: hand.p2_rank)))
    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main(p1p2, example_only=False)
