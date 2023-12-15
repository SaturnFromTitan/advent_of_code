import collections

Boxes = collections.defaultdict[int, dict[str, int]]


def main(file_name: str) -> None:
    with open(file_name) as f:
        texts = f.read().split(",")
    filled_boxes = get_filled_boxes(texts)

    answer = score_boxes(filled_boxes)
    print(f"THE ANSWER IS: {answer}")


def get_filled_boxes(texts: list[str]) -> Boxes:
    boxes: Boxes = collections.defaultdict(dict)
    for text in texts:
        label, operator, focal_length = parse_text(text)
        box_number = my_hash(label)
        if operator == "=":
            boxes[box_number][label] = focal_length
        elif label in boxes[box_number]:
            del boxes[box_number][label]
    return boxes


def parse_text(text: str) -> tuple[str, str, int]:
    label_chars = []
    operator = ""
    value_chars = []
    for char in text:
        if char.isdigit():
            value_chars.append(char)
        elif char in "-=":
            operator = char
        else:
            label_chars.append(char)

    if not (value_str := "".join(value_chars)):
        value_str = "0"
    return "".join(label_chars), operator, int(value_str)


def my_hash(text: str) -> int:
    value = 0
    for char in text:
        value += ord(char)
        value *= 17
        value = value % 256
    return value


def score_boxes(filled_boxes: Boxes) -> int:
    score = 0
    for box_number in range(256):
        lenses = filled_boxes.get(box_number, {})
        for index, focal_length in enumerate(lenses.values()):
            score += (box_number + 1) * (index + 1) * focal_length
    return score


if __name__ == "__main__":
    main("input.txt")
