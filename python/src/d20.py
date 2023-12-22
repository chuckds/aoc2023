"""
Advent Of Code 2023 Day 20
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple, Type

import utils


class Pulse(NamedTuple):
    is_high: bool
    from_module: str
    to_module: str


@dataclass
class Module:
    name: str
    connections: tuple[str, ...]
    mod_type: str

    def get_pulses(self, is_high: bool) -> list[Pulse]:
        return [Pulse(is_high, self.name, conn) for conn in self.connections]

    def add_connection_from(self, from_module: str) -> None:
        pass

    def proc_pulse(self, pulse: Pulse) -> list[Pulse]:
        return self.get_pulses(is_high=pulse.is_high)


@dataclass
class FlipFlop(Module):
    is_on: bool = False

    def proc_pulse(self, pulse: Pulse) -> list[Pulse]:
        if pulse.is_high:
            return []
        self.is_on = not self.is_on
        return self.get_pulses(is_high=self.is_on)


@dataclass
class Conjunction(Module):
    prev_pulse: dict[str, bool] = field(default_factory=dict)

    def proc_pulse(self, pulse: Pulse) -> list[Pulse]:
        self.prev_pulse[pulse.from_module] = pulse.is_high
        high_pulse = not all(self.prev_pulse.values())
        return self.get_pulses(is_high=high_pulse)

    def add_connection_from(self, from_module: str) -> None:
        self.prev_pulse[from_module] = False


TYPE_TO_CLASS: dict[str, Type[Module]] = {"%": FlipFlop, "&": Conjunction, "": Module}


def mod_from_line(line: str) -> Module:
    tname, conns = line.split(" -> ")
    if tname[0] in ("%", "&"):
        mod_type, name = tname[0], tname[1:]
    else:
        mod_type, name = "", tname
    return TYPE_TO_CLASS[mod_type](name, tuple(conns.split(", ")), mod_type)


def press_button(modules: dict[str, Module]) -> tuple[int, int] | None:
    low_pulses = high_pulses = 0
    pulses = deque([Pulse(False, "button", "broadcaster")])
    while pulses:
        pulse = pulses.popleft()
        if pulse.is_high:
            high_pulses += 1
        else:
            low_pulses += 1
            if pulse.to_module == "rx":
                return None
        if dest_mod := modules.get(pulse.to_module):
            pulses.extend(dest_mod.proc_pulse(pulse))
    return low_pulses, high_pulses


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    modules = {
        (mod := mod_from_line(line)).name: mod
        for line in input_file.read_text().splitlines()
    }

    do_p2 = False
    for mod in modules.values():
        for conn in mod.connections:
            if conn_mod := modules.get(conn):
                conn_mod.add_connection_from(mod.name)
            elif conn == "rx":
                do_p2 = True

    pulse_counts: tuple[int, ...] = (0, 0)
    for button_presses in range(1000):
        pulse_counts = tuple(a + b for a, b in zip(press_button(modules), pulse_counts))  # type: ignore[arg-type]
    if do_p2 and False:
        while pulse_counts is not None:
            button_presses += 1
            pulse_counts = press_button(modules)
    return (math.prod(pulse_counts), button_presses + 1)


if __name__ == "__main__":
    utils.per_day_main(p1p2, "")
