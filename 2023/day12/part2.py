import collections
import time

PLACEHOLDER = "?"


def main(file_name: str) -> None:
    with open(file_name) as f:
        answer = parse_file(f)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> int:
    summed = 0
    for num, line in enumerate(f.readlines(), start=1):
        symbols, counts_part = line.strip().split()
        counts = [int(val) for val in counts_part.split(",")]

        print(num, end=": ")
        # summed += get_num_solutions(symbols, counts)
        summed += get_num_solutions("?".join([symbols] * 5), counts * 5)
    return summed


def get_num_solutions(input_symbols: str, target_counts: list[int]) -> int:
    print(f"{input_symbols} - {target_counts}")
    # search_space_size = 2 ** input_symbols.count(PLACEHOLDER)
    # print(input_symbols)
    # print()

    explored = 0
    num_solutions = 0
    queue = collections.deque([input_symbols])
    while queue:
        old_symbols = queue.popleft()

        for new_symbol in "#.":
            symbols = old_symbols.replace(PLACEHOLDER, new_symbol, 1)

            if PLACEHOLDER not in symbols:
                if get_counts(symbols) == target_counts:
                    # print(symbols)
                    num_solutions += 1
                explored += 1
                continue

            if not can_be_valid(symbols, target_counts):
                explored += 2 ** symbols.count(PLACEHOLDER)
                continue

            queue.appendleft(symbols)
            # print(f"{symbols}  ({explored / search_space_size:.1%} explored)")
    print("\tsolutions found:", num_solutions)
    return num_solutions


def can_be_valid(symbols: str, target_counts: list[int]) -> bool:
    if symbols.startswith(PLACEHOLDER):
        return True

    num_missing_hashes = sum(target_counts) - symbols.count("#")
    num_missing_dots = max(0, len(target_counts) - _count_groups(symbols))
    if num_missing_dots + num_missing_hashes > symbols.count(PLACEHOLDER):
        return False

    left_of_placeholder = symbols.split(PLACEHOLDER)[0]
    left_counts = get_counts(left_of_placeholder)
    if not left_counts:
        return True
    elif len(left_counts) > len(target_counts):
        return False

    if left_of_placeholder[-1] == ".":
        return left_counts[: len(left_counts)] == target_counts[: len(left_counts)]
    return (
        left_counts[: len(left_counts) - 1] == target_counts[: len(left_counts) - 1]
        and left_counts[-1] <= target_counts[len(left_counts) - 1]
    )


def _count_groups(symbols: str) -> int:
    groups = 0
    last_char = "."
    for char in symbols:
        if char != "." and (last_char == "."):
            groups += 1
        last_char = char
    return groups


def get_counts(symbols: str) -> list[int]:
    return [len(group) for group in symbols.split(".") if group]


if __name__ == "__main__":
    assert get_counts("#.#.###") == [1, 1, 3]
    assert get_counts(".#...#....###.") == [1, 1, 3]

    assert can_be_valid(".###.##.#.#?", [3, 2, 1]) is False
    assert can_be_valid("..?..??...?##.", [1, 1, 3]) is True
    assert can_be_valid("?###????????", [3, 2, 1]) is True
    assert can_be_valid("####????????", [3, 2, 1]) is False
    assert can_be_valid(".####???????", [3, 2, 1]) is False
    assert can_be_valid(".###.???????", [3, 2, 1]) is True
    assert not can_be_valid("..??#??????..???#??????", [3, 1, 2, 4, 1, 3, 1])
    assert not can_be_valid(".##.#...???#??????", [2, 4, 1, 3, 1])
    assert not can_be_valid(".##.#...#??#??????", [2, 4, 1, 3, 1])

    assert get_num_solutions("???.###", [1, 1, 3]) == 1
    assert get_num_solutions(".??..??...?##.", [1, 1, 3]) == 4
    assert get_num_solutions("?#?#?#?#?#?#?#?", [1, 3, 1, 6]) == 1
    assert get_num_solutions("????.#...#...", [4, 1, 1]) == 1
    assert get_num_solutions("????.######..#####.", [1, 6, 5]) == 4
    assert get_num_solutions("?###????????", [3, 2, 1]) == 10
    assert get_num_solutions("#??????..???#??????", [2, 4, 1, 3, 1]) == 11
    print("all test cases succeeded")

    start = time.monotonic()
    main("input.txt")
    print("time elapsed:", round(time.monotonic() - start, 1))
