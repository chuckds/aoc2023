import importlib

import pytest
from utils import get_all_days, AnswerEntry


def process_answer_entry(entry: AnswerEntry) -> None:
    day_mod = importlib.__import__(entry.module_name)
    part_function = getattr(day_mod, entry.function_name)
    assert part_function(entry.input_file) == entry.expected_result


@pytest.mark.parametrize("entry", get_all_days(examples=True))
def test_puzzle_examples(entry: AnswerEntry) -> None:
    process_answer_entry(entry)


@pytest.mark.parametrize("entry", get_all_days(examples=False))
def test_puzzles(entry: AnswerEntry) -> None:
    process_answer_entry(entry)
