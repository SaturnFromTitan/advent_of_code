import ast
import functools
import itertools


def main():
    with open("input.txt") as f:
        packets = parse_file(f)

    # add extra packets
    extra1 = [[2]]
    extra2 = [[6]]
    packets += [extra1, extra2]

    ordered_packets = sorted(packets, key=functools.cmp_to_key(is_ordered))

    # +1 because the task demands 1-based indices
    idx1 = ordered_packets.index(extra1) + 1
    idx2 = ordered_packets.index(extra2) + 1
    answer = idx1 * idx2
    print(f"THE ANSWER IS: {answer}")


def parse_file(f):
    packets = list()
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue
        parsed_line = ast.literal_eval(line)
        packets.append(parsed_line)
    return packets


def is_ordered(left, right):
    """Compare two packets"""
    for val1, val2 in itertools.zip_longest(left, right):
        # left is shorter than right
        if val1 is None:
            return -1

        # right is shorter than left
        if val2 is None:
            return 1

        res = _is_ordered(val1, val2)
        if res != 0:
            return res
    return 0


def _is_ordered(val1, val2):
    """Compare two values of packets"""
    if isinstance(val1, int) and isinstance(val2, int):
        if val1 == val2:
            return 0
        elif val1 < val2:
            return -1
        else:
            return 1

    if isinstance(val1, int):
        val1 = [val1]
    if isinstance(val2, int):
        val2 = [val2]

    return is_ordered(val1, val2)


if __name__ == '__main__':
    main()
