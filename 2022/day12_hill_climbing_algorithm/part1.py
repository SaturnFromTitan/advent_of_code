import string

from collections import deque
from dataclasses import dataclass
from typing import Iterator

Location = tuple[int, int]
NodeMapping = dict[Location, "Node"]


LETTER_VALUES = {letter: index for index, letter in enumerate(string.ascii_lowercase)}
LETTER_VALUES["S"] = 0
LETTER_VALUES["E"] = 25


def convert_letter_to_value(char: str) -> int:
    return LETTER_VALUES[char]


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    _raw_value: str

    @property
    def value(self):
        return convert_letter_to_value(self._raw_value)

    def reachable_neighbours(self, nodes: NodeMapping) -> Iterator["Node"]:
        for location in self._potential_neighbour_positions():
            if location not in nodes:
                # location is outside the grid
                continue

            neighbour = nodes[location]
            if self._is_reachable(neighbour):
                yield neighbour

    def _potential_neighbour_positions(self) -> list[tuple[int, int]]:
        return [
            (self.x + 1, self.y),
            (self.x - 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1),
        ]

    def _is_reachable(self, other: "Node") -> bool:
        return self.value + 1 >= other.value

    @property
    def location(self):
        return self.x, self.y

    def __str__(self):
        return f"{self._raw_value} at ({self.x}, {self.y})"


def main():
    with open("input.txt") as f:
        nodes, start, target = parse_file(f)

    answer = find_best_path(nodes, start, target)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> tuple[NodeMapping, Node, Node]:
    nodes = dict()
    start = None
    target = None

    for row, line in enumerate(f.readlines()):
        line = line.strip()

        for col, char in enumerate(line):
            node = Node(x=row, y=col, _raw_value=char)
            nodes[(node.x, node.y)] = node

            if char == "S":
                start = node
            elif char == "E":
                target = node

    return nodes, start, target


def find_best_path(nodes: NodeMapping, start: Node, target: Node) -> int:
    visited_nodes: dict[Node, int] = {start: 0}
    queue = deque([start])

    while queue:
        node = queue.popleft()
        node_distance = visited_nodes[node]

        for neighbour in node.reachable_neighbours(nodes):
            # if this node was already seen, then the saved value must be lower than
            # or equal to the new value -> we can ignore it this time
            if neighbour in visited_nodes:
                continue

            if neighbour == target:
                return node_distance + 1

            queue.append(neighbour)
            visited_nodes[neighbour] = node_distance + 1
    raise ValueError("Didn't find a path to 'E'")


if __name__ == '__main__':
    main()
