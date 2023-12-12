import collections
import time

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

        summed += get_num_solutions("?".join([symbols] * 5), counts * 5)
    return summed


def get_num_solutions(input_symbols: str, target_counts: list[int]) -> int:
    print(f"findings solutions for '{input_symbols}' {target_counts}")
    num_solutions = 0
    queue = collections.deque([input_symbols])
    while queue:
        old_symbols = queue.popleft()

        for new_symbol in "#.":
            symbols = old_symbols.replace(PLACEHOLDER, new_symbol, 1)

            if PLACEHOLDER not in symbols:
                if get_counts(symbols) == target_counts:
                    num_solutions += 1
                continue

            if not can_be_valid(symbols, target_counts):
                continue

            queue.appendleft(symbols)
    print(num_solutions)
    return num_solutions


def can_be_valid(symbols: str, target_counts: list[int]) -> bool:
    if symbols.startswith("?"):
        return True

    left_to_placeholder = symbols.split("?")[0]
    left_counts = get_counts(left_to_placeholder)
    if not left_counts:
        return True
    elif len(left_counts) > len(target_counts):
        return False

    return (
        left_counts[: len(left_counts) - 1] == target_counts[: len(left_counts) - 1]
        and left_counts[-1] <= target_counts[len(left_counts) - 1]
    )


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

    assert get_num_solutions("???.###", [1, 1, 3]) == 1
    assert get_num_solutions(".??..??...?##.", [1, 1, 3]) == 4
    assert get_num_solutions("?#?#?#?#?#?#?#?", [1, 3, 1, 6]) == 1
    assert get_num_solutions("????.#...#...", [4, 1, 1]) == 1
    assert get_num_solutions("????.######..#####.", [1, 6, 5]) == 4
    assert get_num_solutions("?###????????", [3, 2, 1]) == 10
    # TODO: how to solve this??
    assert (
        asdf := get_num_solutions(
            "#??????..???#???????#??????..???#???????#??????..???#???????#??????..???#???????#??????..???#??????",
            [2, 4, 1, 3, 1, 2, 4, 1, 3, 1, 2, 4, 1, 3, 1, 2, 4, 1, 3, 1, 2, 4, 1, 3, 1],
        )
    ) == 10, asdf

    print("all test cases succeeded")

    start = time.monotonic()
    main("input.txt")
    print("time elapsed:", round(time.monotonic() - start, 1))
