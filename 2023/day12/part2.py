import functools
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

        summed += get_num_solutions("?".join([symbols] * 5), tuple(counts * 5))
    return summed


@functools.cache
def get_num_solutions(input_symbols: str, target_counts: tuple[int, ...]) -> int:
    if not input_symbols and not target_counts:
        return 1

    num_solutions = 0
    for new_symbol in "#.":
        symbols = input_symbols.replace(PLACEHOLDER, new_symbol, 1)

        if PLACEHOLDER not in symbols and get_counts(symbols) == target_counts:
            num_solutions += 1
            return num_solutions

        if not can_be_valid(symbols, target_counts):
            continue

        remainder, remaining_targets = get_remainders(symbols, target_counts)
        if not remainder and remaining_targets:
            continue

        num_solutions += get_num_solutions(remainder, remaining_targets)
    return num_solutions


def can_be_valid(symbols: str, target_counts: tuple[int, ...]) -> bool:
    if symbols.startswith(PLACEHOLDER):
        return True

    num_missing_hashes = sum(target_counts) - symbols.count("#")
    num_missing_dots = max(0, len(target_counts) - count_groups(symbols))
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


def count_groups(symbols: str) -> int:
    groups = 0
    last_char = "."
    for char in symbols:
        if char != "." and (last_char == "."):
            groups += 1
        last_char = char
    return groups


def get_counts(symbols: str) -> tuple[int, ...]:
    return tuple(len(group) for group in symbols.split(".") if group)


def get_remainders(
    symbols: str, target_counts: tuple[int, ...]
) -> tuple[str, tuple[int, ...]]:
    index_placeholder = symbols.index(PLACEHOLDER)
    left_part = symbols[:index_placeholder]
    remainder = symbols[index_placeholder:]
    if not left_part:
        return symbols, target_counts

    left_counts = get_counts(left_part)
    hashes_before_remainder = count_hashes_at_end(left_part)
    if hashes_before_remainder:
        required_hashes_at_start = target_counts[len(left_counts) - 1] - left_counts[-1]
        if (
            # can't place enough #'s
            len(remainder) < required_hashes_at_start
            # can't place enough #'s
            or "." in remainder[:required_hashes_at_start]
            # string continues, but it's impossible to finish the group with a .
            or (
                len(remainder) > required_hashes_at_start
                and remainder[required_hashes_at_start] == "#"
            )
        ):
            return "", (1,)

        # after the required amount of hashes there needs to be a dot
        remainder = remainder[required_hashes_at_start + 1 :]
    return remainder.lstrip("."), target_counts[len(left_counts) :]


def count_hashes_at_end(symbols: str):
    counter = 0
    for char in symbols[::-1]:
        if char == "#":
            counter += 1
        else:
            break
    return counter


if __name__ == "__main__":
    assert get_counts("#.#.###") == (1, 1, 3)
    assert get_counts(".#...#....###.") == (1, 1, 3)

    assert can_be_valid(".###.##.#.#?", (3, 2, 1)) is False
    assert can_be_valid("..?..??...?##.", (1, 1, 3)) is True
    assert can_be_valid("?###????????", (3, 2, 1)) is True
    assert can_be_valid("####????????", (3, 2, 1)) is False
    assert can_be_valid(".####???????", (3, 2, 1)) is False
    assert can_be_valid(".###.???????", (3, 2, 1)) is True
    assert not can_be_valid("..??#??????..???#??????", (3, 1, 2, 4, 1, 3, 1))
    assert not can_be_valid(".##.#...???#??????", (2, 4, 1, 3, 1))
    assert not can_be_valid(".##.#...#??#??????", (2, 4, 1, 3, 1))

    assert get_num_solutions("???.###", (1, 1, 3)) == 1
    assert get_num_solutions(".??..??...?##.", (1, 1, 3)) == 4
    assert get_num_solutions("#?#?#?#?", (1, 6)) == 1
    assert get_num_solutions("?#?#?#?#?#?#?#?", (1, 3, 1, 6)) == 1

    assert get_num_solutions("????.#...#...", (4, 1, 1)) == 1
    assert get_num_solutions("????.######..#####.", (1, 6, 5)) == 4
    assert get_num_solutions("?###????????", (3, 2, 1)) == 10
    assert get_num_solutions("#??????..???#??????", (2, 4, 1, 3, 1)) == 11

    assert count_hashes_at_end(".#..###") == 3
    assert count_hashes_at_end(".#..##?") == 0
    assert count_hashes_at_end(".") == 0

    assert get_remainders("?###????????", (3, 2, 1)) == ("?###????????", (3, 2, 1))
    assert get_remainders(".###????????", (3, 2, 1)) == ("???????", (2, 1))
    assert get_remainders(".###????????", (5, 2, 1)) == ("?????", (2, 1))
    assert get_remainders(".###?.??????", (5, 2, 1)) == ("", (1,))
    assert get_remainders(".###??#?????", (5, 2, 1)) == ("", (1,))

    print("all test cases succeeded")

    start = time.monotonic()
    main("input.txt")
    print("time elapsed:", round(time.monotonic() - start, 1), "seconds")
