from pathlib import Path

file_name = Path("input.txt")


def main():
    with open(file_name) as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f):
    top3_calories = list()
    current_elf_calories = 0

    for line in f.readlines():
        line = line.replace("\n", "")
        # empty line is an elf separator
        if not line:
            top3_calories = update_max_calories(top3_calories, current_elf_calories)
            current_elf_calories = 0
            continue

        line_calorie = int(line)
        current_elf_calories += line_calorie

    # the file might not end with an empty line
    top3_calories = update_max_calories(top3_calories, current_elf_calories)
    return sum(top3_calories)


def update_max_calories(top3_calories, current_elf_calories):
    if len(top3_calories) < 3:
        top3_calories.append(current_elf_calories)
        return top3_calories

    min_top_calories = min(top3_calories)
    if current_elf_calories > min_top_calories:
        top3_calories.remove(min_top_calories)
        top3_calories.append(current_elf_calories)
    return top3_calories


if __name__ == "__main__":
    main()
