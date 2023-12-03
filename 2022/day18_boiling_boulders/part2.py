from collections import namedtuple, deque

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
        if neighbour not in lava_points and not is_enclosed(neighbour, lava_points):
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


def is_enclosed(point, lava_points):
    # breath-first search to find a way to the outside
    x_values = [point.x for point in lava_points]
    y_values = [point.y for point in lava_points]
    z_values = [point.z for point in lava_points]
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)
    min_z, max_z = min(z_values), max(z_values)

    visited_nodes = {point}
    queue = deque([point])
    while queue:
        node = queue.popleft()

        for neighbour in direct_neighbours(node):
            if neighbour in lava_points:
                # we're only interested in air
                continue

            if neighbour in visited_nodes:
                continue

            if (
                node.x in [min_x, max_x]
                or node.y in [min_y, max_y]
                or node.z in [min_z, max_z]
            ):
                # reached the outside
                return False

            queue.append(neighbour)
            visited_nodes.add(neighbour)
    return True


if __name__ == '__main__':
    main()
