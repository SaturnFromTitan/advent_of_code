from pathlib import Path

file_name = Path("input.txt")


def main():
    with open(file_name) as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f):
    max_calories = 0
    current_elf_calories = 0

    for line in f.readlines():
        line = line.replace("\n", "")
        # empty line is an elf separator
        if not line:
            max_calories = max(max_calories, current_elf_calories)
            current_elf_calories = 0
            continue

        line_calorie = int(line)
        current_elf_calories += line_calorie

    # the file might not end with an empty line
    max_calories = max(max_calories, current_elf_calories)
    return max_calories


if __name__ == "__main__":
    main()
