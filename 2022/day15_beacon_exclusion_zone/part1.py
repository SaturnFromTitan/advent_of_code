import re
from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])


def main():
    with open("input.txt") as f:
        sensor_distances, beacon_points = parse_file(f)
    answer = covered_points(sensor_distances, beacon_points)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> tuple[dict[Point, int], set[Point]]:
    beacon_points: set[Point] = set()
    sensor_distances: dict[Point, int] = dict()
    for line in f.readlines():
        line = line.strip()

        groups = re.match(".+x=(-?\d+), y=(-?\d+).+x=(-?\d+), y=(-?\d+)", line).groups()
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, groups)
        sensor = Point(sensor_x, sensor_y)
        beacon = Point(beacon_x, beacon_y)
        sensor_distances[sensor] = manhattan_distance(sensor, beacon)
        beacon_points.add(beacon)
    return sensor_distances, beacon_points


def manhattan_distance(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def covered_points(sensor_distances: dict[Point, int], beacon_points: set[Point]) -> int:
    max_distance = max(sensor_distances.values())
    sensor_points = sensor_distances.keys()
    min_x = min([sensor.x for sensor in sensor_points])
    max_x = max([sensor.x for sensor in sensor_points])

    start_x = min_x - max_distance
    end_x = max_x + max_distance
    print(start_x, end_x)

    counter = 0
    y = 2_000_000
    for x_offset in range(end_x - start_x + 1):
        x = start_x + x_offset
        point = Point(x, y)

        if point in beacon_points:
            continue

        for sensor, sensor_reach in sensor_distances.items():
            if manhattan_distance(sensor, point) <= sensor_reach:
                counter += 1
                break
    return counter


if __name__ == '__main__':
    main()
