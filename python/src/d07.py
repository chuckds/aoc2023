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


def calc_p1_type(hand: str) -> HandType:
    card_count = Counter(hand)
    match len(card_count):
        case 1:
            return HandType.FIVE_KIND
        case 2:
            return HandType.FOUR_KIND if card_count.most_common(1)[0][1] == 4 else HandType.FULL_HOUSE
        case 3:
            return HandType.THREE_KIND if card_count.most_common(1)[0][1] == 3 else HandType.TWO_PAIR
        case 4:
            return HandType.ONE_PAIR
        case _:
            return HandType.HIGH_CARD


def calc_p2_type(hand: str, p1_type: HandType) -> HandType | int:
    match hand.count("J"):
        case 4:
            return HandType.FIVE_KIND
        case 3:
            # Either at 3-kind or full house, go to 4-kind or 5-kind
            return p1_type + 2
        case 2:
            match p1_type:
                case HandType.FULL_HOUSE | HandType.ONE_PAIR:
                    return p1_type + 2  # Go to five-kind or 3-kind
                case HandType.TWO_PAIR:
                    return p1_type + 3  # Go to 4 kind
                case _:
                    assert False
        case 1:
            match p1_type:
                case HandType.HIGH_CARD | HandType.FOUR_KIND:
                    return p1_type + 1
                case _:
                    return p1_type + 2
        case _:  # 5 | 0
            return p1_type


def hand_to_val(hand: str, order: dict[str, int]) -> int:
    return sum(order[card] * 13**exponent for exponent, card in enumerate(hand[::-1]))


def get_hand_ranks(hand: str) -> tuple[HandRank, HandRank]:
    p1_type = calc_p1_type(hand)
    return (HandRank(p1_type, hand_to_val(hand, CARD_TO_ORDER)),
            HandRank(calc_p2_type(hand, p1_type), hand_to_val(hand, CARD_TO_ORDER_P2)))


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
