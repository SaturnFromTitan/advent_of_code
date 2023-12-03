import ast
import itertools


def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> int:
    pair_counter = 0
    result = 0
    right_orders = list()

    pair = list()
    for line in f.readlines():
        line = line.strip()
        if line:
            parsed_line = ast.literal_eval(line)
            pair.append(parsed_line)
            continue

        pair_counter += 1
        if is_ordered(*pair):
            right_orders.append(pair_counter)
            result += pair_counter

        del pair[:]
    return result


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


if __name__ == "__main__":
    main()
