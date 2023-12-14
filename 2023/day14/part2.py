import itertools
import typing


class Point(typing.NamedTuple):
    row: int
    col: int


def main(file_name: str) -> None:
    with open(file_name) as f:
        block = parse_file(f)
    cycled_block = get_block_after_one_billion_cycles(block)
    answer = score_block(cycled_block)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> str:
    return f.read().strip()


def get_block_after_one_billion_cycles(block: str) -> str:
    target_num = int(1e9)

    # using a dict, so we can look up via hashes, but still have guaranteed order
    previous_blocks = {block: None}
    cycle_length = 0
    cycle_offset = 0
    for i in itertools.count(start=1):
        block = full_cycle(block)
        if block in previous_blocks:
            cycle_offset = list(previous_blocks.keys()).index(block)
            cycle_length = i - cycle_offset
            break

        previous_blocks[block] = None

    assert cycle_length
    offset = (target_num - cycle_offset) % cycle_length
    for _ in range(offset):
        block = full_cycle(block)
    return block


def full_cycle(block: str) -> str:
    for _ in range(4):
        block = tilt_right(rotate_right_90(block))
    return block


def rotate_right_90(block: str) -> str:
    rows = block.split("\n")
    num_rows = len(rows)
    num_cols = len(rows[0])

    # Create an empty grid with switched dimensions
    new_grid = [["" for _ in range(num_rows)] for _ in range(num_cols)]

    # Fill the new grid with characters rotated 90 degrees to the right
    for i in range(num_rows):
        for j in range(num_cols):
            new_grid[j][num_rows - i - 1] = rows[i][j]

    # Convert the grid back to a string
    rotated_block = "\n".join("".join(row) for row in new_grid)
    return rotated_block


def tilt_right(block: str) -> str:
    new_rows = [_tilt_right(row) for row in block.split("\n")]
    return "\n".join(new_rows)


def _tilt_right(row: str) -> str:
    return "#".join("".join(sorted(part)) for part in row.split("#"))


def score_block(block: str) -> int:
    rows = block.split("\n")

    summed = 0
    for row_index, row in enumerate(rows):
        for char in row:
            if char == "O":
                summed += len(rows) - row_index
    return summed


if __name__ == "__main__":
    assert (res := _tilt_right("O....#....")) == "....O#....", res
    print("all test cases passed")

    main("input.txt")
