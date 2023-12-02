import argparse
import importlib
import inspect
import json
import time
import timeit
from pathlib import Path
from typing import Any, NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ANSWER_FILE = REPO_ROOT / "answers.json"
INPUT_DIR = REPO_ROOT / "input"


class AnswerEntry(NamedTuple):
    module_name: str
    function_name: str
    input_file: Path
    expected_result: Any

    def is_example(self) -> bool:
        return "example" in str(self.input_file)


def get_all_days(examples: bool) -> list[AnswerEntry]:
    day_parts = []
    for fields in json.loads(ANSWER_FILE.read_text()):
        entry = AnswerEntry(*fields)
        if isinstance(entry.expected_result, list):
            entry = entry._replace(expected_result=tuple(entry.expected_result))

        if (entry.is_example() and examples) or (not entry.is_example() and not examples):
            day_parts.append(
                entry._replace(input_file=INPUT_DIR / entry.input_file)
            )

    return day_parts


def _input_path(from_file: str, subdir: str) -> Path:
    day_name = Path(from_file).stem
    return INPUT_DIR / subdir / day_name


def real_input(day: str = "") -> Path:
    return _input_path(day if day else inspect.stack()[1].filename, "real")


def example_input(day: str = "") -> Path:
    return _input_path(day if day else inspect.stack()[1].filename, "examples")


def per_day_main(day: str = "") -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true", help="Example only")
    parser.add_argument("--real", action="store_true", help="Real only")
    args = parser.parse_args()
    day = day if day else Path(inspect.stack()[1].filename).stem

    def _get_day_info(day: str) -> list[AnswerEntry]:
        day_info = []
        for example in (True, False):
            for entry in get_all_days(example):
                if entry.module_name == day:
                    day_info.append(entry)
        return day_info

    day_answers = _get_day_info(day)
    day_mod = importlib.__import__(day)
    to_check = []
    for answer in day_answers:
        if answer.is_example() and args.real or (not answer.is_example() and args.example):
            continue
        part_function = getattr(day_mod, answer.function_name)
        start = time.perf_counter()
        result = part_function(answer.input_file)
        name = "example" if answer.is_example() else "real"
        duration = time.perf_counter() - start
        print(f"{name} = {result} (in {duration:.3f}s)")
        to_check.append((answer.expected_result, result, name))
    for expected_result, result, name in to_check:
        assert (
            expected_result == result
        ), f"{day}-{name} result wrong, expected: {expected_result} got {result}"


def run_all() -> None:
    timing_data = []
    test_calls = []
    for answer in get_all_days(False):
        day_mod = importlib.__import__(answer.module_name)
        part_function = getattr(day_mod, answer.function_name)
        ti = timeit.Timer(lambda: part_function(answer.input_file))
        num_calls, time_taken = ti.autorange()
        timing_data.append((time_taken / num_calls, num_calls, time_taken, answer.module_name))
        test_calls.append((part_function, answer.input_file))

    ALL_COUNT = 1
    all_days = timeit.timeit(
        lambda: [day(input) for day, input in test_calls], number=ALL_COUNT
    )

    for avg_time, num_calls, total_time, day in sorted(timing_data, reverse=True):
        print(f"{day} avg {avg_time:.9f} ({num_calls} calls in {total_time:.9f})")

    print(
        f"All {len(test_calls)} days take {all_days / ALL_COUNT:.9f} on average ({ALL_COUNT} calls in {all_days:.9f})"
    )
    return


if __name__ == "__main__":
    run_all()
