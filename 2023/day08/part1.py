import dataclasses
import itertools
import typing
from pathlib import Path

FILE_NAME = Path("input.txt")


@dataclasses.dataclass
class Node:
    id: str
    left: str
    right: str


def main() -> None:
    with open(FILE_NAME) as f:
        instructions, nodes = parse_file(f)

    num_steps = walk(instructions, nodes)
    print(f"THE ANSWER IS: {num_steps}")


def parse_file(f) -> tuple[typing.Iterable[str], dict[str, Node]]:
    instructions, nodes_part = f.read().strip().split("\n\n")

    nodes = {}
    for line in nodes_part.split("\n"):
        node_id, neighbours_part = line.split(" = ")
        left_node_id, right_node_id = neighbours_part.strip(" ()").split(", ")
        nodes[node_id] = Node(id=node_id, left=left_node_id, right=right_node_id)
    return itertools.cycle(instructions), nodes


def walk(instructions: typing.Iterable[str], nodes: dict[str, Node]) -> int:
    _num_steps = 0
    current_node = "AAA"
    for _num_steps, instruction in enumerate(instructions, start=1):
        if instruction == "L":
            current_node = nodes[current_node].left
        else:
            current_node = nodes[current_node].right

        if current_node == "ZZZ":
            break
    return _num_steps


if __name__ == "__main__":
    main()
