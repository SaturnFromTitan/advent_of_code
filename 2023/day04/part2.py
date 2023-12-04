import collections
import itertools
from pathlib import Path

FILE_NAME = Path("input.txt")


def main() -> None:
    with open(FILE_NAME) as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> int:
    total_num_cards = 0
    copies: collections.deque[int] = collections.deque([])
    for line in f.readlines():
        num_card_copies = copies.popleft() if copies else 0
        num_cards = 1 + num_card_copies
        total_num_cards += num_cards

        num_matching_numbers = get_number_of_matching_numbers(line)
        extra_copies = [num_cards] * num_matching_numbers
        copies_temp = []
        for num_copies, num_extra_copies in itertools.zip_longest(
            copies, extra_copies, fillvalue=0
        ):
            copies_temp.append(num_copies + num_extra_copies)
        copies = collections.deque(copies_temp)
    return total_num_cards


def get_number_of_matching_numbers(line: str) -> int:
    _, number_part = line.split(": ")
    winning_numbers_part, my_numbers_part = number_part.split(" | ")
    winning_numbers = set(winning_numbers_part.strip().split())
    my_numbers = set(my_numbers_part.strip().split())
    return len(winning_numbers & my_numbers)


if __name__ == "__main__":
    main()
