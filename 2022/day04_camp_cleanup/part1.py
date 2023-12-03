

def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f):
    total = 0
    for line in f.readlines():
        line = line.strip()

        sections1, sections2 = line.split(",")
        sections1_min, sections1_max = sections1.split("-")
        sections2_min, sections2_max = sections2.split("-")

        sections1_min, sections1_max, sections2_min, sections2_max = int(sections1_min), int(sections1_max), int(sections2_min), int(sections2_max)

        first_in_second = sections1_min >= sections2_min and sections1_max <= sections2_max
        second_in_first = sections2_min >= sections1_min and sections2_max <= sections1_max
        if first_in_second or second_in_first:
            total += 1
    return total


if __name__ == '__main__':
    main()
