import string

PRIOS = {letter: index + 1 for index, letter in enumerate(string.ascii_letters)}


def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f):
    total = 0

    for line in f.readlines():
        line = line.strip()

        items1, items2 = split_items(line)
        common_item = get_common_item(items1, items2)
        priority = determine_priority(common_item)
        total += priority

    return total


def split_items(items):
    assert len(items) % 2 == 0, "must be divisible by 2"
    middle = int(len(items) / 2)
    return items[:middle], items[middle:]


def get_common_item(items1, items2):
    commons = set(items1) & set(items2)
    assert len(commons) == 1
    return list(commons)[0]


def determine_priority(item):
    return PRIOS[item]


if __name__ == "__main__":
    main()
