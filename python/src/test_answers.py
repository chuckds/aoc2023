import pytest
import importlib

from pathlib import Path
from typing import Any

from utils import get_puzzle_info


@pytest.mark.parametrize("day,part,input_file,result", get_puzzle_info(True))
def test_puzzle_examples2(day: str, part: str, input_file: str, result: Any) -> None:
    day_mod = importlib.__import__(day)
    part_function = getattr(day_mod, part)
    assert part_function(Path(input_file)) == result


@pytest.mark.parametrize("day,part,input_file,result", get_puzzle_info(False))
def test_puzzles(day: str, part: str, input_file: str, result: Any) -> None:
    day_mod = importlib.__import__(day)
    part_function = getattr(day_mod, part)
    assert part_function(Path(input_file)) == result
