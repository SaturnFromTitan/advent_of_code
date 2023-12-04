from pathlib import Path

FILE_NAME = Path("input.txt")


def main() -> None:
    with open(FILE_NAME) as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> int:
    summed = 0
    for line in f.readlines():
        _, number_part = line.split(": ")
        winning_numbers_part, my_numbers_part = number_part.split(" | ")
        winning_numbers = set(winning_numbers_part.strip().split())
        my_numbers = set(my_numbers_part.strip().split())
        matching_numbers = winning_numbers & my_numbers
        if matching_numbers:
            summed += 2 ** (len(matching_numbers) - 1)
    return summed


if __name__ == "__main__":
    main()
