"""
Advent Of Code 2023 Day 8
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import NamedTuple, Generator

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

    def next_node(self, start: Node) -> Generator[tuple[Node, int], None, None]:
        location = start
        while True:
            for dir_idx, direction in enumerate(self.directions):
                location = self.node_map[location[direction]]
                if dir_idx + 1 == len(self.directions):
                    yield location, 0
                else:
                    yield location, dir_idx + 1


def get_loop_info(start: Node, md: MapData) -> int:
    steps_to_end = 0
    seen = {(start, 0): 0}
    for node_idx_pair in md.next_node(start):
        next_node = node_idx_pair[0]
        if node_idx_pair in seen:
            break
        if next_node.name.endswith("Z"):
            steps_to_end = len(seen)  # In theory this should be a list but for our inputs this is fine
        seen[node_idx_pair] = len(seen)
    return steps_to_end


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    lines = input_file.read_text().splitlines()
    nodes = (Node.from_line(line) for line in lines[2:])
    md = MapData([DIR_TO_IDX[dir] for dir in lines[0]],
                 {node.name: node for node in nodes})
    start = md.node_map.get("AAA", None)
    p1 = 0
    if start:
        end = md.node_map["ZZZ"]
        for next_node, _ in md.next_node(start):
            p1 += 1
            if next_node == end:
                break

    starts = [node for node in md.node_map.values() if node.name.endswith("A")]
    loops = (
        get_loop_info(start, md) for start in starts
    )
    p2 = math.lcm(*loops)
    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main(p1p2, example_only=False)
