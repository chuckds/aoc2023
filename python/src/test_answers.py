import importlib

import pytest
from utils import AnswerEntry, get_all_days, process_result


def _process_answer_entry(entry: AnswerEntry) -> None:
    day_mod = importlib.__import__(entry.module_name)
    assert entry.function_name is not None
    part_function = getattr(day_mod, entry.function_name)
    process_result(entry, part_function(entry.input_file))


@pytest.mark.parametrize("entry", get_all_days(examples=True))
def test_puzzle_examples(entry: AnswerEntry) -> None:
    _process_answer_entry(entry)


@pytest.mark.parametrize("entry", get_all_days(examples=False))
def test_puzzles(entry: AnswerEntry) -> None:
    _process_answer_entry(entry)
