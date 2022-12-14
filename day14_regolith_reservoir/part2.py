import functools
import itertools


Point = tuple[int, int]

SAND_SOURCE = (500, 0)


def main():
    with open("input.txt") as f:
        rock_points = parse_file(f)

    answer = simulate_sand_flow(rock_points)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> set[Point]:
    point_separator = " -> "

    rock_points = set()
    for line in f.readlines():
        line = line.strip()

        path_coordinates = [parse_coordinates(pair) for pair in line.split(point_separator)]
        rock_points |= points_from_path(path_coordinates)
    return rock_points


def parse_coordinates(text: str) -> Point:
    x, y = text.split(",")
    return int(x), int(y)


def points_from_path(path_coordinates: list[Point]) -> set[Point]:
    points = set()
    for point1, point2 in pairwise(path_coordinates):
        min_x, max_x = min(point1[0], point2[0]), max(point1[0], point2[0])
        min_y, max_y = min(point1[1], point2[1]), max(point1[1], point2[1])
        for x_offset, y_offset in itertools.product(
            range(max_x - min_x + 1) or [min_x],
            range(max_y - min_y + 1) or [min_y],
        ):
            x = min_x + x_offset
            y = min_y + y_offset
            points.add((x, y))
    return points


def pairwise(iterable):
    """itertools.pairwise isn't available in 3.9 yet..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def simulate_sand_flow(rock_points: set[Point]) -> int:
    max_rock_y = max([point[1] for point in rock_points])
    bottom_y = max_rock_y + 2

    sand_rest_points: set[Point] = set()
    current_sand = SAND_SOURCE
    while SAND_SOURCE not in sand_rest_points:
        _is_blocked = functools.partial(
            is_blocked,
            rock_points=rock_points,
            sand_rest_points=sand_rest_points,
            bottom_y=bottom_y
        )

        if not _is_blocked((current_sand[0], current_sand[1] + 1)):
            # straight down
            current_sand = (current_sand[0], current_sand[1] + 1)
        elif not _is_blocked((current_sand[0] - 1, current_sand[1] + 1)):
            # diagonally down left
            current_sand = (current_sand[0] - 1, current_sand[1] + 1)
        elif not _is_blocked((current_sand[0] + 1, current_sand[1] + 1)):
            # diagonally down right
            current_sand = (current_sand[0] + 1, current_sand[1] + 1)
        else:
            # sand can't move, so it comes to a rest
            sand_rest_points.add(current_sand)
            current_sand = SAND_SOURCE
    visualise(rock_points, set(sand_rest_points))
    return len(sand_rest_points)


def is_blocked(point, rock_points, sand_rest_points, bottom_y):
    blocked_points = rock_points | sand_rest_points
    return (point in blocked_points) or (point[1] >= bottom_y)


def visualise(rock_points, sand_rest_points):
    blocked_points = rock_points | sand_rest_points | {SAND_SOURCE}
    x_coordinates = [p[0] for p in blocked_points]
    y_coordinates = [p[1] for p in blocked_points]
    min_x, max_x = min(x_coordinates), max(x_coordinates)
    min_y, max_y = min(y_coordinates), max(y_coordinates)

    chars = ""
    for y_offset, x_offset in itertools.product(
        range(max_y - min_y + 1),
        range(max_x - min_x + 1),
    ):
        x = min_x + x_offset
        y = min_y + y_offset
        point = (x, y)
        if point in rock_points:
            chars += "#"
        elif point in sand_rest_points:
            chars += "o"
        elif point == SAND_SOURCE:
            chars += "+"
        else:
            chars += "."

    line_length = max_x - min_x + 1
    lines = [chars[i:i+line_length] for i in range(0, len(chars), line_length)]
    for line in lines:
        print(line)


if __name__ == '__main__':
    main()
