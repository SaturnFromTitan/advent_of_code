import typing
from pathlib import Path

file_name = Path("input.txt")

DigitChar = typing.Literal["1", "2", "3", "4", "5", "6", "7", "8", "9"]
SPELLED_DIGITS: dict[str, DigitChar] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
SPELLED_DIGITS_REVERSED = {k[::-1]: v for (k, v) in SPELLED_DIGITS.items()}


def main() -> None:
    with open(file_name) as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> int:
    summed = 0
    for raw_line in f.readlines():
        line = raw_line.strip()
        first_digit = get_first_digit(line)
        last_digit = get_first_digit(line, reverse=True)

        row_value = int(f"{first_digit}{last_digit}")
        summed += row_value
    return summed


def get_first_digit(text: str, reverse: bool = False) -> DigitChar:
    if reverse:
        text = text[::-1]
        digit_mapping = SPELLED_DIGITS_REVERSED
    else:
        digit_mapping = SPELLED_DIGITS

    for i, char in enumerate(text):
        for spelled_digit, digit in digit_mapping.items():
            if char == digit or text[i : i + len(spelled_digit)] == spelled_digit:
                return digit
    raise ValueError(f"Couldn't find a digit in '{text}'")


if __name__ == "__main__":
    main()
