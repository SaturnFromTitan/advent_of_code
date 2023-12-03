import itertools
from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])

SAND_SOURCE = Point(500, 0)


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
    return Point(int(x), int(y))


def points_from_path(path_coordinates: list[Point]) -> set[Point]:
    points = set()
    for point1, point2 in itertools.pairwise(path_coordinates):
        min_x, max_x = min(point1.x, point2.x), max(point1.x, point2.x)
        min_y, max_y = min(point1.y, point2.y), max(point1.y, point2.y)
        for x_offset, y_offset in itertools.product(
            range(max_x - min_x + 1) or [min_x],
            range(max_y - min_y + 1) or [min_y],
        ):
            x = min_x + x_offset
            y = min_y + y_offset
            points.add(Point(x, y))
    return points


def simulate_sand_flow(rock_points: set[Point]) -> int:
    max_rock_y = max([point.y for point in rock_points])
    bottom_y = max_rock_y + 2
    num_rocks = len(rock_points)

    blocked_points = rock_points.copy()
    current_sand = SAND_SOURCE
    while SAND_SOURCE not in blocked_points:
        if not is_blocked(temp := Point(current_sand.x, current_sand.y + 1), blocked_points, bottom_y):
            # straight down
            current_sand = temp
        elif not is_blocked(temp := Point(current_sand.x - 1, current_sand.y + 1), blocked_points, bottom_y):
            # diagonally down left
            current_sand = temp
        elif not is_blocked(temp := Point(current_sand.x + 1, current_sand.y + 1), blocked_points, bottom_y):
            # diagonally down right
            current_sand = temp
        else:
            # sand can't move, so it comes to a rest
            blocked_points.add(current_sand)
            current_sand = SAND_SOURCE
    # visualise(rock_points, blocked_points)
    return len(blocked_points) - num_rocks


def is_blocked(point, blocked_points, bottom_y):
    return (point in blocked_points) or (point.y >= bottom_y)


def visualise(rock_points, blocked_points):
    sand_rest_points = blocked_points - rock_points
    all_points = blocked_points | {SAND_SOURCE}

    x_coordinates = [p.x for p in all_points]
    y_coordinates = [p.y for p in all_points]
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
