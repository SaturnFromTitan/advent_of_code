import itertools
import re
from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])


def main():
    with open("input.txt") as f:
        sensor_distances, beacon_points = parse_file(f)
    point = find_distress_beacon(sensor_distances, beacon_points)

    answer = point.x * 4_000_000 + point.y
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


def find_distress_beacon(sensor_distances: dict[Point, int], beacon_points: set[Point]) -> Point:
    relevant_points = set()
    for sensor, reach in sensor_distances.items():
        perimeter_points(sensor, reach + 1, relevant_points)
        print("Number of relevant points in frame:", len(relevant_points))
        print("*" * 100)

    for point in relevant_points:
        if point in beacon_points:
            continue

        is_covered = False
        for sensor, sensor_reach in sensor_distances.items():
            if manhattan_distance(sensor, point) <= sensor_reach:
                is_covered = True
                break

        if not is_covered:
            return point
    raise ValueError


def perimeter_points(point: Point, radius: int, points: set[Point]):
    print(point, "with radius:", radius)
    for x_offset, y_offset in zip(range(radius + 1), range(radius + 1)):
        north1 = Point(point.x - radius + x_offset, point.y - y_offset)
        if is_in_frame(north1):
            points.add(north1)

        north2 = Point(point.x + radius - x_offset, point.y - y_offset)
        if is_in_frame(north2):
            points.add(north2)

        south1 = Point(point.x - radius + x_offset, point.y + y_offset)
        if is_in_frame(south1):
            points.add(south1)

        south2 = Point(point.x + radius - x_offset, point.y + y_offset)
        if is_in_frame(south2):
            points.add(south2)


def is_in_frame(point: Point) -> bool:
    return (0 <= point.x <= 4_000_000) and (0 <= point.y <= 4_000_000)


if __name__ == '__main__':
    main()
