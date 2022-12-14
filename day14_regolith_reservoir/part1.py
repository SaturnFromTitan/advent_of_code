import itertools


Point = tuple[int, int]


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
    sand_source = (500, 0)

    sand_rest_points: set[Point] = set()
    current_sand = sand_source
    while current_sand[1] <= max_rock_y:
        blocked_points = rock_points | sand_rest_points
        if (current_sand[0], current_sand[1] + 1) not in blocked_points:
            # straight down
            current_sand = (current_sand[0], current_sand[1] + 1)
        elif (current_sand[0] - 1, current_sand[1] + 1) not in blocked_points:
            # diagonally down left
            current_sand = (current_sand[0] - 1, current_sand[1] + 1)
        elif (current_sand[0] + 1, current_sand[1] + 1) not in blocked_points:
            # diagonally down right
            current_sand = (current_sand[0] + 1, current_sand[1] + 1)
        else:
            # sand can't move, so it comes to a rest
            sand_rest_points.add(current_sand)
            current_sand = sand_source
    return len(sand_rest_points)


if __name__ == '__main__':
    main()
