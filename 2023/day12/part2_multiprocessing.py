import collections
import multiprocessing
import time
from pprint import pprint

PLACEHOLDER = "?"


def main(file_name: str) -> None:
    with open(file_name) as f:
        condition_records = parse_file(f)

    pool = multiprocessing.Pool()

    solutions = pool.starmap(get_num_solutions, condition_records)

    pool.close()
    pool.join()

    pprint(solutions)
    print(f"THE ANSWER IS: {sum(solutions)}")


def parse_file(f) -> list[tuple[str, list[int]]]:
    records = []
    for line in f.readlines():
        symbols, counts_part = line.strip().split()
        counts = [int(val) for val in counts_part.split(",")]
        records.append((PLACEHOLDER.join([symbols] * 5), counts * 5))
    return records


def get_num_solutions(input_symbols: str, target_counts: list[int]) -> int:
    print(f"{input_symbols} - {target_counts}")
    explored = 0
    num_solutions = 0
    queue = collections.deque([input_symbols])
    while queue:
        old_symbols = queue.popleft()

        for new_symbol in "#.":
            symbols = old_symbols.replace(PLACEHOLDER, new_symbol, 1)

            if PLACEHOLDER not in symbols:
                if get_counts(symbols) == target_counts:
                    num_solutions += 1
                explored += 1
                continue

            if not can_be_valid(symbols, target_counts):
                explored += 2 ** symbols.count(PLACEHOLDER)
                continue

            queue.appendleft(symbols)
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
    start = time.monotonic()
    main("input.txt")
    print("time elapsed:", round(time.monotonic() - start, 1))
