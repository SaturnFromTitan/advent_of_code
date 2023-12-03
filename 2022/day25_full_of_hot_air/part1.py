def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> str:
    snafu_numbers = [line.strip() for line in f.readlines()]
    decimal_numbers = [to_decimal(snafu) for snafu in snafu_numbers]
    summed = sum(decimal_numbers)
    return to_snafu(summed)


SNAFU_MAPPING = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}
INVERSE_SNAFU_MAPPING = {v: k for (k, v) in SNAFU_MAPPING.items()}


def to_decimal(snafu: str) -> int:
    summed = 0
    for i, char in enumerate(snafu[::-1]):
        converted = SNAFU_MAPPING[char]
        summed += converted * (5**i)
    return summed


def to_snafu(quotient: int) -> str:
    if quotient == 0:
        return str(quotient)

    bits = list()
    while quotient != 0:
        quotient, remainder = divmod(quotient + 2, 5)
        snafu_remainder = INVERSE_SNAFU_MAPPING[remainder - 2]
        bits.append(snafu_remainder)
    return "".join([str(bit) for bit in bits[::-1]])


if __name__ == "__main__":
    main()
