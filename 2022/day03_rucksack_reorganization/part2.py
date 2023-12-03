import string

PRIOS = {letter: index + 1 for index, letter in enumerate(string.ascii_letters)}


def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f):
    total = 0

    group = list()
    for line in f.readlines():
        line = line.strip()

        group.append(set(line))
        if len(group) == 3:
            common_item = get_common_item(*group)
            priority = determine_priority(common_item)
            total += priority

            # reset group
            group = list()
    assert not group
    return total


def get_common_item(items1, items2, items3):
    commons = items1 & items2 & items3
    assert len(commons) == 1
    return list(commons)[0]


def determine_priority(item):
    return PRIOS[item]


if __name__ == "__main__":
    main()
