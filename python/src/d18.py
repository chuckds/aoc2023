"""
Advent Of Code 2023 Day 18
"""

from __future__ import annotations

import enum
from pathlib import Path
from typing import Generator, Iterable, NamedTuple

import utils


class Direction(enum.Enum):
    NORTH = (0, 1)
    SOUTH = (0, -1)
    WEST = (-1, 0)
    EAST = (1, 0)

    def opposite(self) -> Direction:
        return Direction((self.value[0] * -1, self.value[1] * -1))


DIR_TO_LEFT = {dir: Direction((-1 * dir.value[1], dir.value[0])) for dir in Direction}
DIR_TO_RIGHT = {dir: Direction((dir.value[1], -1 * dir.value[0])) for dir in Direction}


class Coord(NamedTuple):
    col: int
    line: int

    def in_direction(self, direction: Direction, scale: int = 1) -> Coord:
        return Coord(self.col + direction.value[0] * scale,
                     self.line + direction.value[1] * scale)

    def adjacent(self) -> Generator[Coord, None, None]:
        for a_dir in Direction:
            yield self.in_direction(a_dir)


class Heading(NamedTuple):
    loc: Coord
    direction: Direction


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


def print_points(points: Iterable[Coord], char: str = "#") -> None:
    points = set(points)
    min_line = min(c.line for c in points)
    max_line = max(c.line for c in points)
    min_col = min(c.col for c in points)
    for line in range(max_line, min_line - 1, -1):
        # line_min_col = min(c.col for c in points if c.line == line)
        # print(" " * (line_min_col - min_col), end="")
        for col in range(min_col, max(c.col for c in points if c.line == line) + 1):
            pchar = char if Coord(col, line) in points else " "
            print(pchar, end="")
        print()


def is_inside(point: Coord, loop: Iterable[Coord]) -> bool:
    try:
        min_line = min(c.line for c in loop if c.col == point.col)
    except ValueError:
        # None of the loop is in the same columne - must be outide
        return False
    crossed = 0
    for line_num in range(min_line - 1, point.line + 1):
        if Coord(point.col, line_num) in loop:
            crossed += 1
    return (crossed % 2) == 1


def find_enclosed_ground(trench_loop: list[Heading]) -> set[Coord]:
    left_trench = set()
    right_trench = set()
    loop_locs = set(h.loc for h in trench_loop)
    for loop_idx, loop_head in enumerate(trench_loop):
        left_spot = loop_head.loc.in_direction(DIR_TO_LEFT[loop_head.direction])
        if left_spot not in loop_locs:
            left_trench.add(left_spot)
        right_spot = loop_head.loc.in_direction(DIR_TO_RIGHT[loop_head.direction])
        if right_spot not in loop_locs:
            right_trench.add(right_spot)
        straight_on = loop_head.loc.in_direction(loop_head.direction)
        if straight_on not in loop_locs:
            if (
                left_spot == trench_loop[(loop_idx + 1) % len(trench_loop)].loc
            ):  # Going left
                right_trench.add(straight_on)
            else:  # Not going straight on or left, can't go backwards so must be right
                left_trench.add(straight_on)

    left_inside = [p for p in left_trench if is_inside(p, loop_locs)]
    right_inside = [p for p in right_trench if is_inside(p, loop_locs)]
    if len(right_inside) < len(left_inside):
        result = left_trench
    else:
        result = right_trench
    # print_points(loop_locs)
    # print("-"*10)
    # print_points(result)
    # Expand the set to include any ground that wasn't adjacent to the pipe loop
    to_scan = set(result)
    while to_scan:
        point = to_scan.pop()
        for adj_point in point.adjacent():
            if adj_point not in loop_locs and adj_point not in result:
                result.add(adj_point)
                to_scan.add(adj_point)
    return result


def get_loop(insts: list[Instruction]) -> list[Heading]:
    coord = Coord(0, 0)
    loop: list[Heading] = []
    for inst in insts:
        for _ in range(inst.dist):
            coord = coord.in_direction(inst.direction)
            loop.append(Heading(coord, inst.direction))
    return loop


def sf(verticies: list[Coord]) -> int:
    return [0 if a_vert.col == b_vert.col else ((a_vert.col - b_vert.col + 2) * (a_vert.line + b_vert.line))
            for a_vert, b_vert in zip(verticies, verticies[1:])]

def shoestring(verticies: list[Coord]) -> int:
    vals = sf(verticies)
    return abs(sum(vals)) // 2


def get_verticies(insts: list[Instruction]) -> list[Coord]:
    coord = Coord(0, 0)
    verticies = [coord]
    for inst in insts:
        coord = coord.in_direction(inst.direction, inst.dist)
        verticies.append(coord)
    return verticies


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    instructions = [
        Instruction.from_line(line) for line in input_file.read_text().splitlines()
    ]
    p2_insts = [inst.p2_inst() for inst in instructions]

    verticies = get_verticies(instructions)
    loop = get_loop(instructions)
    enclosed = find_enclosed_ground(loop)
    #p2_loop = get_loop(p2_insts)
    return (len(enclosed) + len(loop), None)


if __name__ == "__main__":
    utils.per_day_main(p1p2, "example")
