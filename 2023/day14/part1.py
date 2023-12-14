import typing


class Point(typing.NamedTuple):
    row: int
    col: int


def main(file_name: str) -> None:
    with open(file_name) as f:
        blocks = parse_file(f)
    answer = sum([score_block(block) for block in blocks])
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> list[str]:
    return f.read().strip().split("\n\n")


def score_block(block: str) -> int:
    # operate on columns
    columns = get_columns(block)
    return sum([score_column(column) for column in columns])


def get_columns(block: str) -> list[list[str]]:
    rows = block.split("\n")
    return [[row[i] for row in rows if row[i]] for i in range(len(rows[0]))]


def score_column(column: list[str]) -> int:
    stone_position = -1
    score = 0
    for index, char in enumerate(column):
        if char == "#":
            stone_position = index
        elif char == "O":
            score += len(column) - stone_position - 1
            stone_position += 1
    return score


if __name__ == "__main__":
    main("input.txt")
