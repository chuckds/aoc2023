"""
Advent Of Code 2023 Day 8
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

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


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    lines = input_file.read_text().splitlines()
    directions = [DIR_TO_IDX[dir] for dir in lines[0]]

    nodes = (Node.from_line(line) for line in lines[2:])
    node_map = {node.name: node for node in nodes}

    location = node_map.get("AAA", None)
    p1 = 0
    if location:
        end = node_map["ZZZ"]
        while location != end:
            for direction in directions:
                p1 += 1
                location = node_map[location[direction]]
                if location == end:
                    break

    locations = [node for node in node_map.values() if node.name.endswith("A")]
    p2 = 0
    while locations:
        for direction in directions:
            p2 += 1
            new_locations = [
                node_map[location[direction]]
                for location in locations
            ]
            if all(node.name.endswith("Z") for node in new_locations):
                locations = []
                break
            locations = new_locations
    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main(p1p2, example_only=True)
