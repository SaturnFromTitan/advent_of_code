import itertools


def main(file_name: str) -> None:
    with open(file_name) as f:
        patterns = parse_file(f)
    answer = sum([score(pattern) for pattern in patterns])
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> list[str]:
    return f.read().strip().split("\n\n")


def score(pattern: str) -> int:
    rows = pattern.split("\n")
    double_rows = check_rows(rows)
    double_columns = check_columns(rows)
    return 100 * double_rows + double_columns


def check_rows(lines: list[str]) -> int:
    reflection_candidates = []
    for index, (row1, row2) in enumerate(itertools.pairwise(lines)):
        if row1 == row2:
            reflection_candidates.append(index)

    for idx in reflection_candidates:
        length = min(len(lines) - 1 - idx, idx + 1)
        if all(
            lines[idx - offset] == lines[idx + 1 + offset]
            for offset in range(1, length)
        ):
            return idx + 1
    return 0


def check_columns(rows: list[str]) -> int:
    columns = ["".join([row[i] for row in rows]) for i in range(len(rows[0]))]
    return check_rows(columns)


if __name__ == "__main__":
    main("input.txt")
