def main(file_name: str) -> None:
    with open(file_name) as f:
        texts = f.read().split(",")
    answer = sum([score_text(text) for text in texts])
    print(f"THE ANSWER IS: {answer}")


def score_text(text: str) -> int:
    value = 0
    for char in text:
        value += ord(char)
        value *= 17
        value = value % 256
    return value


if __name__ == "__main__":
    main("input.txt")
