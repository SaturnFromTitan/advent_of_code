import ast
import itertools


def main():
    with open("input.txt") as f:
        packets = parse_file(f)

    # add extra packets
    extra1 = [[2]]
    extra2 = [[6]]
    packets += [extra1, extra2]

    ordered_packets = sort(packets)

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


def sort(packets):
    sorted_packets = list()
    for packet in packets:

        inserted = False
        for idx, temp_packet in enumerate(sorted_packets):
            res = is_ordered(packet, temp_packet)
            if res is None:
                raise ValueError(f"Found two identical packets: {packet}")

            if res:
                sorted_packets.insert(idx, packet)
                inserted = True
                break
        if not inserted:
            sorted_packets.append(packet)
    return sorted_packets


def is_ordered(left, right):
    """Compare two packets"""
    for val1, val2 in itertools.zip_longest(left, right):
        # left is shorter than right
        if val1 is None:
            return True

        # right is shorter than left
        if val2 is None:
            return False

        res = _is_ordered(val1, val2)
        if res is not None:
            return res
    return None


def _is_ordered(val1, val2):
    """Compare two values of packets"""
    if isinstance(val1, int) and isinstance(val2, int):
        if val1 == val2:
            return None
        return val1 < val2

    if isinstance(val1, int):
        val1 = [val1]
    if isinstance(val2, int):
        val2 = [val2]

    return is_ordered(val1, val2)


if __name__ == '__main__':
    main()
