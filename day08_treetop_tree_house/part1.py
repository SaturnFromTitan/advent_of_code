from typing import Iterable

Location = tuple[int, int]
Matrix = list[list[int]]


def main():
    matrix = parse_file()
    horizontal_visibles = process_horizontally(matrix)
    vertical_visibles = process_horizontally(transpose(matrix))
    answer = len(horizontal_visibles | vertical_visibles)
    print(f"THE ANSWER IS: {answer}")


def parse_file() -> Matrix:
    matrix = list()
    with open("input.txt") as f:
        for line in f.readlines():
            heights = [int(char) for char in line.strip()]
            matrix.append(heights)
    return matrix


def transpose(matrix: Matrix) -> Matrix:
    return list(map(list, zip(*matrix)))


def process_horizontally(matrix: Matrix) -> set[Location]:
    visibles = set()
    for row_index, heights in enumerate(matrix):
        visibles |= check_horizontally(heights, row_index)
        visibles |= check_horizontally(reversed(heights), row_index)
    return visibles


def check_horizontally(heights: Iterable[int], row_index: int) -> set[Location]:
    visibles: set[Location] = set()
    line_max_from_left = -1
    for col_index, tree_height in enumerate(heights):
        if tree_height > line_max_from_left:
            line_max_from_left = tree_height
            visibles.add((row_index, col_index))
    return visibles


if __name__ == '__main__':
    main()
