import itertools
import typing


class Point(typing.NamedTuple):
    row: int
    col: int


def main(file_name: str) -> None:
    with open(file_name) as f:
        galaxy_points = parse_file(f)
    galaxy_points = expand_space(galaxy_points)
    answer = get_sum_of_shortest_distances(galaxy_points)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> list[Point]:
    return [
        Point(row_index, col_index)
        for row_index, line in enumerate(f.readlines())
        for col_index, symbol in enumerate(line.strip())
        if symbol == "#"
    ]


def expand_space(points: list[Point]) -> list[Point]:
    rows_with_points = {p.row for p in points}
    max_row = max(rows_with_points)
    rows_without_points = set(range(max_row)) - rows_with_points

    cols_with_points = {p.col for p in points}
    max_col = max(cols_with_points)
    cols_without_points = set(range(max_col)) - cols_with_points

    new_points = []
    for point in points:
        num_expanded_rows_before = len(
            {row for row in rows_without_points if row < point.row}
        )
        num_expanded_cols_before = len(
            {col for col in cols_without_points if col < point.col}
        )
        new_point = Point(
            row=point.row + num_expanded_rows_before * (int(1e6) - 1),
            col=point.col + num_expanded_cols_before * (int(1e6) - 1),
        )
        new_points.append(new_point)
    return new_points


def get_sum_of_shortest_distances(points: list[Point]) -> int:
    summed = 0
    for start, target in itertools.combinations(points, 2):
        summed += get_shortest_distance(start, target)
    return summed


def get_shortest_distance(start: Point, target: Point) -> int:
    return abs(start.row - target.row) + abs(start.col - target.col)


if __name__ == "__main__":
    assert get_shortest_distance(Point(0, 0), Point(0, 0)) == 0
    assert get_shortest_distance(Point(0, 0), Point(1, 0)) == 1
    assert get_shortest_distance(Point(0, 0), Point(0, 1)) == 1
    assert get_shortest_distance(Point(0, 0), Point(-1, 0)) == 1
    assert get_shortest_distance(Point(0, 0), Point(0, -1)) == 1
    assert get_shortest_distance(Point(0, 0), Point(1, 1)) == 2
    assert get_shortest_distance(Point(6, 1), Point(11, 5)) == 9
    print("test cases succeeded!")

    main("input.txt")
