import argparse
import importlib
import inspect
import json
import sys
import time
import timeit
from pathlib import Path
from typing import Any, NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ANSWER_FILE = REPO_ROOT / "answers.json"
INPUT_DIR = REPO_ROOT / "input"


class AnswerEntry(NamedTuple):
    """Info on a days answer."""

    module_name: str
    function_name: str | None
    is_example: bool
    input_file: Path
    expected_result: tuple[Any]
    input_file_suffix: str

    def result_name(self) -> str:
        if self.is_example:
            i_suffix = "-" + self.input_file_suffix if self.input_file_suffix else ""
            input_txt = "exmaple" + i_suffix
        else:
            input_txt = "real"
        return f"{self.module_name}-{input_txt:9s}"


def get_all_days(examples: bool, needs_answer: bool = True) -> list[AnswerEntry]:
    inputs_seen = set()
    day_parts = []
    for (
        module_name,
        function_name,
        is_example,
        expected_result,
        *optional_args,
    ) in json.loads(ANSWER_FILE.read_text()):
        if isinstance(expected_result, list):
            expected_result = tuple(expected_result)
        else:
            expected_result = (expected_result,)

        sub_dir = "examples" if is_example else "real"
        input_file = INPUT_DIR / sub_dir / module_name
        input_file_suffix = ""
        if optional_args:
            input_file_suffix = optional_args[0]
            input_file = input_file.parent / (input_file.name + input_file_suffix)

        inputs_seen.add(input_file)
        if needs_answer and any(res is None for res in expected_result):
            # Only return this answer if all answers are known
            print(f"Skipping {module_name} - {input_file} since not all answers known")
            continue
        if (is_example and examples) or (not is_example and not examples):
            day_parts.append(
                AnswerEntry(
                    module_name,
                    function_name,
                    is_example,
                    input_file,
                    expected_result,
                    input_file_suffix,
                )
            )

    if not needs_answer:
        # Check for any inputs that we don't have answers for yet
        sub_dir = "examples" if examples else "real"
        for input_file in (INPUT_DIR / sub_dir).glob("**/*"):
            if input_file not in inputs_seen:
                day_parts.append(
                    AnswerEntry(
                        input_file.name[:3],
                        None,
                        examples,
                        input_file,
                        (None,),
                        input_file.name[3:],
                    )
                )

    return day_parts


def _input_path(from_file: str, subdir: str) -> Path:
    day_name = Path(from_file).stem
    return INPUT_DIR / subdir / day_name


def real_input(day: str = "") -> Path:
    return _input_path(day if day else inspect.stack()[1].filename, "real")


def example_input(day: str = "") -> Path:
    return _input_path(day if day else inspect.stack()[1].filename, "examples")


def process_result(answer: AnswerEntry, result: Any) -> None:
    if not isinstance(result, tuple):
        result = (result,)
    for part_idx, (expected_result_part, result_part) in enumerate(
        zip(answer.expected_result, result)
    ):
        if expected_result_part is not None and result_part is not None:
            assert (
                expected_result_part == result_part
            ), f"{answer.result_name()}-{part_idx} result wrong, expected: {expected_result_part} got {result_part}"


def per_day_main(
    part_function: Any,
    input_file: str = "",
) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true", help="Example only")
    parser.add_argument("--real", action="store_true", help="Real only")
    parser.add_argument(
        "--repeat", default=1, type=int, help="Number of times to run the test"
    )
    args = parser.parse_args()
    day = Path(inspect.stack()[1].filename).stem

    example_only = input_file == "example" or args.example
    real_only = input_file == "real" or args.real
    input_suffix = "" if input_file in ("example", "real") else input_file

    def _get_day_info(day: str) -> list[AnswerEntry]:
        day_info = []
        for example in (True, False):
            for entry in get_all_days(example, needs_answer=False):
                if entry.module_name == day:
                    day_info.append(entry)
        return day_info

    day_answers = _get_day_info(day)
    to_check = []
    day_mod: Any = None
    for answer in day_answers:
        if answer.is_example and real_only or (not answer.is_example and example_only):
            continue
        if input_suffix and answer.input_file_suffix != input_suffix:
            continue
        if answer.function_name:
            # If the function name is in the answer entry then use that
            # rather than what was passed in
            day_mod = importlib.__import__(day) if day_mod is None else day_mod
            part_function = getattr(day_mod, answer.function_name)
        start = time.perf_counter()
        for _ in range(args.repeat):
            result = part_function(answer.input_file)
        duration = time.perf_counter() - start
        print(
            f"{answer.result_name()} = {result} (in {duration / args.repeat:.3f}s) - expecting {answer.expected_result}"
        )
        to_check.append((answer, result))
    for answer, result in to_check:
        process_result(answer, result)


def _run_all(days: list[str]) -> None:
    """
    Get data from running each day on its own then all days in one go.
    """
    timing_data = []
    test_calls = []
    for answer in get_all_days(False, True):
        assert answer.function_name is not None
        if days and answer.module_name not in days:
            continue
        day_mod = importlib.__import__(answer.module_name)
        part_function = getattr(day_mod, answer.function_name)
        ti = timeit.Timer(lambda: part_function(answer.input_file))
        num_calls, time_taken = ti.autorange()
        timing_data.append(
            (time_taken / num_calls, num_calls, time_taken, answer.module_name)
        )
        test_calls.append((part_function, answer.input_file))

    # Now run all days together
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
    _run_all(sys.argv[1:])
