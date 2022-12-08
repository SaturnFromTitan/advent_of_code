Location = tuple[int, int]
Matrix = list[list[int]]


def main():
    matrix = parse_file()
    horizontal_visibles = process_horizontally(matrix, transposed=False)
    vertical_visibles = process_horizontally(matrix, transposed=True)
    answer = len(horizontal_visibles | vertical_visibles)
    print(f"THE ANSWER IS: {answer}")


def parse_file() -> Matrix:
    matrix = list()
    with open("input.txt") as f:
        for line in f.readlines():
            heights = [int(char) for char in line.strip()]
            matrix.append(heights)
    return matrix


def process_horizontally(matrix: Matrix, transposed: bool) -> set[Location]:
    if transposed:
        matrix = transpose(matrix)

    visibles = set()
    for row_index, heights in enumerate(matrix):
        visibles |= check_horizontally(heights, row_index, from_left=True)
        visibles |= check_horizontally(heights, row_index, from_left=False)

    if transposed:
        return {(col, row) for (row, col) in visibles}
    return visibles


def transpose(matrix: Matrix) -> Matrix:
    return list(map(list, zip(*matrix)))


def check_horizontally(heights: list[int], row_index: int, from_left: bool) -> set[Location]:
    row_length = len(heights)
    if not from_left:
        heights = reversed(heights)

    visibles: set[Location] = set()
    line_max_from_left = -1
    for col_index, tree_height in enumerate(heights):
        if not from_left:
            col_index = row_length - col_index - 1

        if tree_height > line_max_from_left:
            line_max_from_left = tree_height
            visibles.add((row_index, col_index))
    return visibles


if __name__ == '__main__':
    main()
