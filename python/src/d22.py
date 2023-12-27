"""
Advent Of Code 2023 Day 22
"""

from __future__ import annotations

from pathlib import Path
from typing import Generator, NamedTuple, Iterable

import utils


class XYCoord(NamedTuple):
    x: int
    y: int


class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def to_xy(self) -> XYCoord:
        return XYCoord(self.x, self.y)

    @classmethod
    def from_str(cls, string: str) -> Coord:
        return cls(*(int(t) for t in string.split(",")))


class Brick(NamedTuple):
    enda: Coord
    endb: Coord

    def squares(self, num_z_planes: int = -1) -> Generator[tuple[int, XYCoord], None, None]:
        square = self.enda
        yield 0, square.to_xy()
        direction = Coord._make(b - a for a, b in zip(self.enda, self.endb))
        while square != self.endb:
            square = Coord._make(sd + dir // max(direction) for sd, dir in zip(square, direction))
            if num_z_planes == -1 or square.z - self.enda.z + 1 <= num_z_planes:
                yield square.z - self.enda.z, square.to_xy()
            else:
                break

    @classmethod
    def from_line(cls, line: str) -> Brick:
        enda, endb = line.split("~")
        return cls(Coord.from_str(enda), Coord.from_str(endb))


def what_falls_if_removed(
        brick_to_remove: Brick, brick_to_bricks_above: dict[Brick, set[Brick]], brick_to_bricks_below: dict[Brick, set[Brick]]
) -> set[Brick]:
    removed_brick = {brick_to_remove}
    gone_bricks = {brick_to_remove}
    falling_bricks: set[Brick] = set()
    while gone_bricks:
        for dependent_brick in brick_to_bricks_above.get(gone_bricks.pop(), set()):
            if not (brick_to_bricks_below[dependent_brick] - falling_bricks - removed_brick):  # Nothing left to support it
                gone_bricks.add(dependent_brick)
                falling_bricks.add(dependent_brick)

    return falling_bricks


def get_what_rests_on(bricks: Iterable[Brick]) -> dict[Brick, set[Brick]]:
    point_heights: dict[XYCoord, int] = {}
    top_brick_at_point: dict[XYCoord, Brick] = {}
    brick_to_bricks_below: dict[Brick, set[Brick]] = {}
    for brick in sorted(bricks, key=lambda b: min(b.enda.z, b.endb.z)):
        z_level = max(point_heights.get(c, 0) for _, c in brick.squares(1)) + 1
        brick_to_bricks_below[brick] = set()
        for z, c in brick.squares():
            if z == 0:
                rests_on = top_brick_at_point.get(c)
                rest_lvl = point_heights.get(c)
                if rests_on and rest_lvl == z_level - 1:
                    brick_to_bricks_below[brick].add(rests_on)
            point_heights[c] = z_level + z
            top_brick_at_point[c] = brick
    return brick_to_bricks_below


def p1p2(input_file: Path = utils.real_input()) -> tuple[int | None, int | None]:
    bricks = [
        Brick.from_line(line)
        for line in input_file.read_text().splitlines()
    ]

    brick_to_bricks_below = get_what_rests_on(bricks)
    critical_bricks = {
        next(iter(ontop_of)) for _, ontop_of in brick_to_bricks_below.items() if len(ontop_of) == 1
    }
    disintegratable = set(bricks) - critical_bricks

    brick_to_bricks_above: dict[Brick, set[Brick]] = {}
    for brick, bricks_below in brick_to_bricks_below.items():
        for brick_beneath in bricks_below:
            brick_to_bricks_above.setdefault(brick_beneath, set()).add(brick)

    brick_to_num_fall: dict[Brick, int] = {
        brick: len(what_falls_if_removed(brick, brick_to_bricks_above, brick_to_bricks_below))
        for brick in bricks
    }

    return (len(disintegratable), sum(brick_to_num_fall.values()))


if __name__ == "__main__":
    utils.per_day_main(p1p2)
