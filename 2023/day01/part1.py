from pathlib import Path

file_name = Path("input.txt")


def main() -> None:
    with open(file_name) as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> int:
    summed = 0
    for line in f.readlines():
        line_numbers = []
        for char in line:
            if char.isdigit():
                line_numbers.append(char)
        row_value = int(f"{line_numbers[0]}{line_numbers[-1]}")
        summed += row_value
    return summed


if __name__ == "__main__":
    main()
