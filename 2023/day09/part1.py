import itertools
from pathlib import Path

FILE_NAME = Path("input.txt")


def main() -> None:
    with open(FILE_NAME) as f:
        histories = parse_file(f)
    answer = sum(extrapolate_value(values) for values in histories)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> list[list[int]]:
    return [[int(val) for val in line.strip().split()] for line in f.readlines()]


def extrapolate_value(values: list[int]) -> int:
    last_values = [values[-1]]
    while any(val != 0 for val in values):
        values = get_diffs(values)
        last_values.append(values[-1])
    return sum(last_values)


def get_diffs(values: list[int]) -> list[int]:
    return [val2 - val1 for val1, val2 in itertools.pairwise(values)]


if __name__ == "__main__":
    # test cases
    assert get_diffs([0, 3, 6, 9, 12, 15]) == [3, 3, 3, 3, 3]
    assert extrapolate_value([0, 3, 6, 9, 12, 15]) == 18

    main()
