"""
Advent Of Code 2023 Day 8
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Generator, NamedTuple

import utils

DIR_TO_IDX = {"L": 0, "R": 1}


class Node(NamedTuple):
    left: str
    right: str
    name: str

    @classmethod
    def from_line(cls, line: str) -> Node:
        name, paths = line.split(" = ")
        left, right = paths[1:-1].split(", ")
        return Node(left, right, name)


class MapData(NamedTuple):
    directions: list[int]
    node_map: dict[str, Node]

    def next_node(self, start: Node) -> Generator[Node, None, None]:
        location = start
        while True:
            for direction in self.directions:
                location = self.node_map[location[direction]]
                yield location


def get_loop_info(start: Node, md: MapData) -> int:
    """Not sure why this works. All the loops seem to be the same length..."""
    steps_to_end = 0
    for next_node in md.next_node(start):
        steps_to_end += 1
        if next_node.name.endswith("Z"):
            break
    return steps_to_end


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    lines = input_file.read_text().splitlines()
    nodes = (Node.from_line(line) for line in lines[2:])
    md = MapData(
        [DIR_TO_IDX[dir] for dir in lines[0]], {node.name: node for node in nodes}
    )
    start = md.node_map.get("AAA", None)
    p1 = 0
    if start:
        end = md.node_map["ZZZ"]
        for next_node in md.next_node(start):
            p1 += 1
            if next_node == end:
                break

    starts = (node for node in md.node_map.values() if node.name.endswith("A"))
    p2 = math.lcm(*(get_loop_info(start, md) for start in starts))
    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main(p1p2)
