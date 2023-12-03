

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
        sections1_min, sections1_max, sections2_min, sections2_max =\
            int(sections1_min), int(sections1_max), int(sections2_min), int(sections2_max)

        has_overlap = (
            sections1_min <= sections2_min <= sections1_max
            or sections2_min <= sections1_min <= sections2_max
        )
        if has_overlap:
            total += 1
    return total


if __name__ == '__main__':
    main()
