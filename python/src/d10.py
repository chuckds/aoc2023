"""
Advent Of Code 2023 Day 10
"""

from __future__ import annotations

import dataclasses
import enum
from pathlib import Path
from typing import Generator, NamedTuple

import utils


class Direction(enum.Enum):
    NORTH = (0, 1)
    SOUTH = (0, -1)
    WEST = (-1, 0)
    EAST = (1, 0)


DIR_TO_LEFT = {dir: Direction((-1 * dir.value[1], dir.value[0])) for dir in Direction}


DIR_TO_RIGHT = {dir: Direction((dir.value[1], -1 * dir.value[0])) for dir in Direction}


class Coord(NamedTuple):
    col: int
    line: int

    def in_direction(self, direction: Direction) -> Coord:
        return Coord(self.col + direction.value[0], self.line + direction.value[1])

    def adjacent(self) -> Generator[Coord, None, None]:
        for a_dir in Direction:
            yield self.in_direction(a_dir)


CHAR_TO_CONNECTIONS = {
    "|": (Direction.NORTH, Direction.SOUTH),
    "-": (Direction.EAST, Direction.WEST),
    "L": (Direction.NORTH, Direction.EAST),
    "J": (Direction.NORTH, Direction.WEST),
    "7": (Direction.SOUTH, Direction.WEST),
    "F": (Direction.SOUTH, Direction.EAST),
}


@dataclasses.dataclass
class Field:
    grounds: set[Coord] = dataclasses.field(default_factory=set)
    pipe: set[Coord] = dataclasses.field(default_factory=set)
    connected_pipes: dict[Coord, dict[Coord, Direction]] = dataclasses.field(
        default_factory=dict
    )
    start: Coord | None = None
    pipe_loop: set[Coord] = dataclasses.field(default_factory=set)

    @classmethod
    def from_lines(cls, lines: list[str]) -> Field:
        field = cls()
        for line_num, line in enumerate(lines):
            for col_num, char in enumerate(line):
                coord = Coord(col_num + 1, -1 * (line_num + 1))
                if char == "S":
                    field.start = coord
                    field.pipe.add(coord)
                elif dirs := CHAR_TO_CONNECTIONS.get(char, ()):
                    field.connected_pipes[coord] = {
                        coord.in_direction(dir): dir for dir in dirs
                    }
                    field.pipe.add(coord)
                else:
                    field.grounds.add(coord)
        return field


def find_enclosed_ground(
    field: Field, pipe_loop_dirs: list[tuple[Coord, Direction]]
) -> set[Coord]:
    non_loop_pipe = field.pipe - field.pipe_loop
    ground_equiv = field.grounds | non_loop_pipe
    left_grounds = set()
    right_grounds = set()
    for pipe, from_dir in pipe_loop_dirs:
        left_spot = pipe.in_direction(DIR_TO_LEFT[from_dir])
        if left_spot in ground_equiv:
            left_grounds.add(left_spot)
        right_spot = pipe.in_direction(DIR_TO_RIGHT[from_dir])
        if right_spot in ground_equiv:
            right_grounds.add(right_spot)
        straight_on = pipe.in_direction(from_dir)
        if straight_on in ground_equiv:
            if left_spot in field.connected_pipes[pipe]:  # Going left
                right_grounds.add(straight_on)
            else:  # Not going straight on or left, can't go backwards so must be right
                left_grounds.add(straight_on)

    # Assume the smallest set is the enclosed set - seems to work
    result = min(left_grounds, right_grounds, key=len)

    # Expand the set to include any ground that wasn't adjacent to the pipe loop
    to_scan = set(result)
    while to_scan:
        point = to_scan.pop()
        for adj_point in point.adjacent():
            if adj_point in ground_equiv and adj_point not in result:
                result.add(adj_point)
                to_scan.add(adj_point)
    return result


def get_loop(
    start: Coord, connected_pipes: dict[Coord, dict[Coord, Direction]]
) -> list[tuple[Coord, Direction]]:
    # Find a coord that connects to start
    start_adjcent = next(
        (adjacent, connected_pipes[adjacent][start])
        for adjacent in start.adjacent()
        if start in connected_pipes.get(adjacent, {})
    )
    (pipe, to_dir), prev = start_adjcent, start
    from_dir = Direction(*(-1 * v for v in to_dir.value))
    pipe_loop = [(start, from_dir)]
    while pipe != start:  # Walk the loop
        pipe_loop.append((pipe, from_dir))
        (pipe, from_dir), prev = (
            next(
                (p, from_dir)
                for p, from_dir in connected_pipes[pipe].items()
                if p != prev
            ),
            pipe,
        )
    return pipe_loop


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    field = Field.from_lines(input_file.read_text().splitlines())
    assert field.start is not None
    pipe_loop_dirs = get_loop(field.start, field.connected_pipes)
    field.pipe_loop = set(pipe for pipe, _ in pipe_loop_dirs)
    enclosed_ground = find_enclosed_ground(field, pipe_loop_dirs)
    return (len(field.pipe_loop) // 2, len(enclosed_ground))


if __name__ == "__main__":
    utils.per_day_main(p1p2)
