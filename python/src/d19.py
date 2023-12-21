"""
Advent Of Code 2023 Day 19
"""

from __future__ import annotations

import math
import operator
from pathlib import Path
from typing import Callable, NamedTuple

import utils


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_line(cls, line: str) -> Part:
        return cls(*(int(token[2:]) for token in line[1:-1].split(",")))


PART_VAR_IDX = {field: index for index, field in enumerate(Part._fields)}


class PartRange(NamedTuple):
    x: tuple[int, int] = (0, 0)
    m: tuple[int, int] = (0, 0)
    a: tuple[int, int] = (0, 0)
    s: tuple[int, int] = (0, 0)

    def apply_limit(self, lim_idx: int, op: str, val: int, res: bool) -> PartRange | None:
        if (op == "<" and res) or (op == ">" and not res):
            upper_bound = val if op == ">" else (val - 1)
            new_lim = (self[lim_idx][0], min(upper_bound, self[lim_idx][1]))
        else:
            lower_bound = val if op == "<" else (val + 1)
            new_lim = (max(lower_bound, self[lim_idx][0]), self[lim_idx][1])

        if new_lim[1] < new_lim[0]:  # Max is less than min so case is not possible
            return None
        return PartRange._make(
            new_lim if idx == lim_idx else v for idx, v in enumerate(self)
        )


OP_MAP = {
    "<": operator.lt,
    ">": operator.gt,
}


class Condition(NamedTuple):
    func: Callable[[Part], bool]
    result: str
    part_idx: int
    op: str
    val: int

    def split_pv(self, pv: PartRange) -> tuple[PartRange | None, PartRange | None]:
        if self.part_idx < 0:  # This Condition doesn't have a test
            return (pv, None)
        return (
            pv.apply_limit(self.part_idx, self.op, self.val, True),
            pv.apply_limit(self.part_idx, self.op, self.val, False),
        )

    @classmethod
    def from_str(cls, string: str) -> Condition:
        tokens = string.split(":")
        if len(tokens) > 1:
            var, op = tokens[0][:2]  # type: ignore[misc]
            val = int(tokens[0][2:])
            var_idx = PART_VAR_IDX[var]  # type: ignore[has-type]
            return cls(
                lambda part: OP_MAP[op](part[var_idx], val), tokens[1], var_idx, op, val  # type: ignore[has-type]
            )
        return cls(lambda _: True, tokens[0], -1, "", -1)


class Workflow(NamedTuple):
    name: str
    conditions: list[Condition]

    def is_accepted(self, part: Part, workflows: dict[str, Workflow]) -> bool:
        result = next(
            condition.result for condition in self.conditions if condition.func(part)
        )
        if next_workflow := workflows.get(result):
            return next_workflow.is_accepted(part, workflows)
        else:
            return result == "A"

    def accepted_ranges(self, pv: PartRange, workflows: dict[str, Workflow]) -> list[PartRange]:
        accepted_pvs = []
        for condition in self.conditions:
            true_pv, next_pv = condition.split_pv(pv)
            if true_pv:
                if next_workflow := workflows.get(condition.result):
                    accepted_pvs.extend(next_workflow.accepted_ranges(true_pv, workflows))
                elif condition.result == "A":
                    accepted_pvs.append(true_pv)
            if not next_pv:
                break
            pv = next_pv
        return accepted_pvs

    @classmethod
    def from_line(cls, line: str) -> Workflow:
        name, conditions = line.split("{")
        return cls(
            name, [Condition.from_str(tok) for tok in conditions[:-1].split(",")]
        )


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    line_iter = iter(input_file.read_text().splitlines())
    workflows: dict[str, Workflow] = {}
    for line in line_iter:
        if line:
            workflow = Workflow.from_line(line)
            workflows[workflow.name] = workflow
        else:
            break
    parts = [Part.from_line(line) for line in line_iter]
    accepted = (part for part in parts if workflows["in"].is_accepted(part, workflows))

    accepted_ranges = workflows["in"].accepted_ranges(
        PartRange((1, 4000), (1, 4000), (1, 4000), (1, 4000)), workflows
    )
    accepted_combs = (
        math.prod(1 + mx - mn for mn, mx in accepted_range)
        for accepted_range in accepted_ranges
    )
    return (sum(v for part in accepted for v in part), sum(accepted_combs))


if __name__ == "__main__":
    utils.per_day_main(p1p2)
