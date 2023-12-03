Location = tuple[int, int]
ScoreMapping = dict[Location, int]
Matrix = list[list[int]]


def main():
    matrix = parse_file()
    horizontal_scores = process_horizontally(matrix, transposed=False)
    vertical_scores = process_horizontally(matrix, transposed=True)
    scores = merge_scores(horizontal_scores, vertical_scores)
    answer = max(scores.values())
    print(f"THE ANSWER IS: {answer}")


def parse_file() -> Matrix:
    matrix = list()
    with open("input.txt") as f:
        for line in f.readlines():
            heights = [int(char) for char in line.strip()]
            matrix.append(heights)
    return matrix


def process_horizontally(matrix: Matrix, transposed: bool) -> ScoreMapping:
    if transposed:
        matrix = transpose(matrix)

    scores = dict()
    for row_index, heights in enumerate(matrix):
        left_to_right_scores = check_horizontally(heights, row_index, from_left=True)
        right_to_left_scores = check_horizontally(heights, row_index, from_left=False)
        row_scores = merge_scores(left_to_right_scores, right_to_left_scores)
        # keys are distinct
        scores = {**scores, **row_scores}

    if transposed:
        scores = {(col, row): score for (row, col), score in scores.items()}
    return scores


def transpose(matrix: Matrix) -> Matrix:
    return list(map(list, zip(*matrix)))


def check_horizontally(
    heights: list[int], row_index: int, from_left: bool
) -> ScoreMapping:
    row_length = len(heights)
    if not from_left:
        heights = list(reversed(heights))

    scores: ScoreMapping = dict()
    for col_index, tree_height in enumerate(heights):
        value = 0
        for i in range(row_length - col_index - 1):
            value += 1
            next_tree_height = heights[col_index + i + 1]
            if next_tree_height >= tree_height:
                break

        if not from_left:
            col_index = row_length - col_index - 1
        scores[(row_index, col_index)] = value
    return scores


def merge_scores(scores1: ScoreMapping, scores2: ScoreMapping) -> ScoreMapping:
    # assumes they have the same keys
    scores: ScoreMapping = dict()
    for key, value1 in scores1.items():
        value2 = scores2[key]
        scores[key] = value1 * value2
    return scores


if __name__ == "__main__":
    main()
