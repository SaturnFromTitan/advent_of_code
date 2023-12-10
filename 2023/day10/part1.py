import typing


class Location(typing.NamedTuple):
    row: int
    col: int


LocationMap = dict[Location, list[Location]]


def main(file_name: str) -> None:
    with open(file_name) as f:
        location_map, start = parse_file(f)

    answer = walk(location_map, start)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> tuple[LocationMap, Location]:
    location_map: LocationMap = {}
    start_location = None
    for row_index, line in enumerate(f.readlines()):
        for col_index, symbol in enumerate(line.strip()):
            location = Location(row_index, col_index)
            if symbol == "S":
                start_location = location
            location_map[location] = get_neighbour_candidates(location, symbol)

    if not start_location:
        raise ValueError("Didn't find start location")
    return location_map, start_location


def get_neighbour_candidates(location: Location, symbol: str) -> list[Location]:  # noqa: PLR0911
    row, col = location

    if symbol == ".":
        return []
    elif symbol == "|":
        return [Location(row - 1, col), Location(row + 1, col)]
    elif symbol == "-":
        return [Location(row, col - 1), Location(row, col + 1)]
    elif symbol == "L":
        return [Location(row - 1, col), Location(row, col + 1)]
    elif symbol == "J":
        return [Location(row, col - 1), Location(row - 1, col)]
    elif symbol == "7":
        return [Location(row, col - 1), Location(row + 1, col)]
    elif symbol == "F":
        return [Location(row, col + 1), Location(row + 1, col)]
    elif symbol == "S":
        return [
            # going clockwise, starting at 12
            Location(row - 1, col),
            Location(row, col + 1),
            Location(row + 1, col),
            Location(row, col - 1),
        ]
    raise ValueError(f"Unexpected symbol: {symbol}")


def walk(location_map: LocationMap, start: Location) -> int:
    current_location = start
    visited = {start}
    while len(visited) == 1 or current_location != start:
        neighbours = get_neighbours(current_location, location_map)
        unseen_neighbours = neighbours - visited
        if not unseen_neighbours:
            break

        # choose next location
        for neighbour in unseen_neighbours:
            current_location = neighbour
            visited.add(neighbour)
            break
    return len(visited) // 2


def get_neighbours(location: Location, location_map: LocationMap) -> set[Location]:
    neighbour_candidates = location_map[location]
    return {
        candidate
        for candidate in neighbour_candidates
        if location in location_map.get(candidate, [])
    }


if __name__ == "__main__":
    main("input.txt")
