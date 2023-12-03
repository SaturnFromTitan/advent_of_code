"""
    [G]         [P]         [M]
    [V]     [M] [W] [S]     [Q]
    [N]     [N] [G] [H]     [T] [F]
    [J]     [W] [V] [Q] [W] [F] [P]
[C] [H]     [T] [T] [G] [B] [Z] [B]
[S] [W] [S] [L] [F] [B] [P] [C] [H]
[G] [M] [Q] [S] [Z] [T] [J] [D] [S]
[B] [T] [M] [B] [J] [C] [T] [G] [N]
 1   2   3   4   5   6   7   8   9
"""

CRATES = {
    1: ["B", "G", "S", "C"],
    2: ["T", "M", "W", "H", "J", "N", "V", "G"],
    3: ["M", "Q", "S"],
    4: ["B", "S", "L", "T", "W", "N", "M"],
    5: ["J", "Z", "F", "T", "V", "G", "W", "P"],
    6: ["C", "T", "B", "G", "Q", "H", "S"],
    7: ["T", "J", "P", "B", "W"],
    8: ["G", "D", "C", "Z", "F", "T", "Q", "M"],
    9: ["N", "S", "H", "B", "P", "F"],
}


def main():
    with open("input.txt") as f:
        process_file(f)

    answer = generate_message()
    print(f"THE ANSWER IS: {answer}")


def process_file(f):
    for idx, line in enumerate(f.readlines()):
        amount, source, target = map(int, line.split()[1::2])
        crates_to_move = CRATES[source][-amount:]
        CRATES[target] += list(reversed(crates_to_move))
        del CRATES[source][-amount:]


def generate_message():
    message = ""
    for slot in CRATES.values():
        message += slot[-1]
    return message


if __name__ == "__main__":
    main()
