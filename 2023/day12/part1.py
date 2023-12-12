import collections

PLACEHOLDER = "?"


def main(file_name: str) -> None:
    with open(file_name) as f:
        answer = parse_file(f)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> int:
    summed = 0
    for line in f.readlines():
        symbols, counts_part = line.strip().split()
        counts = [int(val) for val in counts_part.split(",")]

        summed += get_num_solutions(symbols, counts)
    return summed


def get_num_solutions(input_symbols: str, target_counts: list[int]) -> int:
    num_solutions = 0
    queue = collections.deque([input_symbols])
    while queue:
        symbols = queue.popleft()

        if PLACEHOLDER not in symbols:
            if get_counts(symbols) == target_counts:
                num_solutions += 1
            continue

        for new_symbol in ".#":
            new_symbols = symbols.replace(PLACEHOLDER, new_symbol, 1)
            queue.appendleft(new_symbols)
    return num_solutions


def get_counts(symbols: str) -> list[int]:
    assert PLACEHOLDER not in symbols
    return [len(group) for group in symbols.split(".") if group]


if __name__ == "__main__":
    assert get_counts("#.#.###") == [1, 1, 3]
    assert get_counts(".#...#....###.") == [1, 1, 3]

    assert get_num_solutions(".??..??...?##.", [1, 1, 3]) == 4
    print("all test cases succeeded")

    main("input.txt")
