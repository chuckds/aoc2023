"""
Advent Of Code 2023 Day 01
"""

from __future__ import annotations

from pathlib import Path

import utils

DIGIT_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
WORD_TO_DIGIT = {word: str(idx + 1) for idx, word in enumerate(DIGIT_WORDS)}

digit_subsets_fwd = {
    word[:num_chars] for word in DIGIT_WORDS for num_chars in range(1, len(word))
}
digit_subsets_back = {
    word[-num_chars:] for word in DIGIT_WORDS for num_chars in range(1, len(word))
}


def get_calibration_values(lines: list[str], part2: bool) -> list[int]:
    calibration_values = []
    for line in lines:
        first = last = "0"
        poss_word = ""
        for char in line:
            if char.isdigit():
                first = char
                break
            elif part2:
                poss_word += char
                first = WORD_TO_DIGIT.get(poss_word, "0")
                if first != "0":
                    break
                elif poss_word not in digit_subsets_fwd:
                    for idx in range(1, len(poss_word)):
                        if poss_word[idx:] in digit_subsets_fwd:
                            poss_word = poss_word[idx:]
                            break
                    else:
                        poss_word = ""
        poss_word = ""
        for char in line[::-1]:
            if char.isdigit():
                last = char
                break
            elif part2:
                poss_word = char + poss_word
                last = WORD_TO_DIGIT.get(poss_word, "0")
                if last != "0":
                    break
                elif poss_word not in digit_subsets_back:
                    for idx in range(1, len(poss_word)):
                        if poss_word[:-idx] in digit_subsets_back:
                            poss_word = poss_word[:-idx]
                            break
                    else:
                        poss_word = ""
        calibration_values.append(int(first + last))
    return calibration_values


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    words = input_file.read_text().splitlines()
    return (
        sum(get_calibration_values(words, False)),
        sum(get_calibration_values(words, True)),
    )


if __name__ == "__main__":
    utils.per_day_main()
