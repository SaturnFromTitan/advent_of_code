from collections import namedtuple

Point = namedtuple("Point", ["x", "y", "z"])


def main():
    with open("input.txt") as f:
        lava_points = parse_file(f)

    answer = get_surface_area(lava_points)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f):
    points = set()
    for line in f.readlines():
        raw_coordinates = line.strip().split(",")
        point = Point(*map(int, raw_coordinates))
        points.add(point)
    return points


def get_surface_area(all_lava_points):
    surface_area = 0
    for lava_point in all_lava_points:
        point_surface_area = get_point_surface_area(lava_point, all_lava_points)
        surface_area += point_surface_area
    return surface_area


def get_point_surface_area(point, lava_points):
    surface_area = 0
    for neighbour in direct_neighbours(point):
        if neighbour not in lava_points:
            surface_area += 1
    return surface_area


def direct_neighbours(point):
    x, y, z = point
    yield Point(x, y, z - 1)
    yield Point(x, y, z + 1)
    yield Point(x, y - 1, z)
    yield Point(x, y + 1, z)
    yield Point(x + 1, y, z)
    yield Point(x - 1, y, z)


if __name__ == "__main__":
    main()
