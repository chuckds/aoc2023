"""
Advent Of Code 2023 Day 18
"""

from __future__ import annotations

import enum
from itertools import pairwise
from pathlib import Path
from typing import NamedTuple

import utils


class Direction(enum.Enum):
    NORTH = (0, 1)
    SOUTH = (0, -1)
    WEST = (-1, 0)
    EAST = (1, 0)


class Coord(NamedTuple):
    col: int
    line: int

    def in_direction(self, direction: Direction, scale: int = 1) -> Coord:
        return Coord(self.col + direction.value[0] * scale,
                     self.line + direction.value[1] * scale)


INST_TO_DIR = {
    "U": Direction.NORTH,
    "D": Direction.SOUTH,
    "L": Direction.WEST,
    "R": Direction.EAST,
}


P2_INST_TO_DIR = {
    "3": Direction.NORTH,
    "1": Direction.SOUTH,
    "2": Direction.WEST,
    "0": Direction.EAST,
}

class Instruction(NamedTuple):
    direction: Direction
    dist: int
    colour: str

    def p2_inst(self) -> Instruction:
        return Instruction(P2_INST_TO_DIR[self.colour[-1]], int(self.colour[:5], 16), "")

    @classmethod
    def from_line(cls, line: str) -> Instruction:
        inst, dist, colour = line.split()
        return cls(INST_TO_DIR[inst], int(dist), colour[2:-1])


def showlace(verticies: list[Coord], perimeter: int) -> int:
    vals = ((b_vert.col - a_vert.col) * (a_vert.line)
            for a_vert, b_vert in pairwise(verticies))
    return int(abs(sum(vals)) - 0.5 * perimeter + 1) + perimeter


def get_verticies(insts: list[Instruction]) -> list[Coord]:
    coord = Coord(0, 0)
    return [coord] + [coord := coord.in_direction(inst.direction, inst.dist) for inst in insts]


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    instructions = [
        Instruction.from_line(line) for line in input_file.read_text().splitlines()
    ]
    p2_instructions = [inst.p2_inst() for inst in instructions]
    return (
        showlace(get_verticies(instructions), sum(inst.dist for inst in instructions)),
        showlace(get_verticies(p2_instructions), sum(inst.dist for inst in p2_instructions)),
    )


if __name__ == "__main__":
    utils.per_day_main(p1p2)
