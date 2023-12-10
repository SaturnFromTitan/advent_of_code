"""
Idea: double the "resolution" of the discrete grid, i.e. add locations at .5

That makes it easy to determine if points are really inside the loop pipes or if they
have a connection to the outside by squeezing between the pipes.

Afterwards, we can count the inner points via BFS or DFS.
"""
import typing


class Location(typing.NamedTuple):
    row: float
    col: float


LocationMap = dict[Location, str]


def main(file_name: str) -> None:
    with open(file_name) as f:
        location_map, start = parse_file(f)

    loop_locations = walk(location_map, start)
    remove_irrelevant_symbols(location_map, loop_locations)
    enclosed_locations = get_enclosed_locations(location_map, loop_locations)
    # only consider the locations from the original grid resolution
    answer = len(
        [
            loc
            for loc in enclosed_locations
            if loc.row.is_integer() and loc.col.is_integer()
        ]
    )
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> tuple[LocationMap, Location]:
    location_map: LocationMap = {}
    start = None
    for row_index, line in enumerate(f.readlines()):
        for col_index, symbol in enumerate(line.strip()):
            location = Location(row_index, col_index)
            if symbol == "S":
                start = location
            location_map[location] = symbol

            # add half-way points. the symbols of these intermediate points just extend
            # the pipe symbol they originate from
            # special handling for 'S' is below (outside the loops)
            # note that this also adds points outside the grid - but we don't mind
            horizontal_halfway_location = Location(location.row, location.col + 0.5)
            horizontal_halfway_symbol = "-" if symbol in "F-L" else "|"
            location_map[horizontal_halfway_location] = horizontal_halfway_symbol

            vertical_halfway_location = Location(location.row + 0.5, location.col)
            vertical_halfway_symbol = "|" if symbol in "F|7" else "-"
            location_map[vertical_halfway_location] = vertical_halfway_symbol

    if not start:
        raise ValueError("Didn't find start location")

    # special handling for start neighbours
    # the half-way points next to the start have to connect start to its neighbours
    # therefore we need to check the int neighbours of start and construct the half-way
    # points accordingly
    north_of_start = Location(start.row - 1, start.col)
    north_symbol = "|" if location_map.get(north_of_start, ".") in "F|7" else "-"
    location_map[Location(start.row - 0.5, start.col)] = north_symbol

    east_of_start = Location(start.row, start.col + 1)
    east_symbol = "-" if location_map.get(east_of_start, ".") in "J-7" else "|"
    location_map[Location(start.row, start.col + 0.5)] = east_symbol

    south_of_start = Location(start.row + 1, start.col)
    south_symbol = "|" if location_map.get(south_of_start, ".") in "LJ|" else "-"
    location_map[Location(start.row + 0.5, start.col)] = south_symbol

    west_of_start = Location(start.row, start.col - 1)
    west_symbol = "-" if location_map.get(west_of_start, ".") in "-FL" else "|"
    location_map[Location(start.row, start.col - 0.5)] = west_symbol

    return location_map, start


def walk(location_map: LocationMap, start: Location) -> set[Location]:
    current_location = start
    visited = {start}
    while len(visited) == 1 or current_location != start:
        neighbours = get_connected_neighbours(current_location, location_map)
        unseen_neighbours = neighbours - visited
        if not unseen_neighbours:
            # implies that we arrived back at start (which we've already seen)
            # this assumes we work with valid input data
            break

        # choose next location
        for neighbour in unseen_neighbours:
            current_location = neighbour
            visited.add(neighbour)
            break
    return visited


def get_connected_neighbours(
    location: Location, location_map: LocationMap
) -> set[Location]:
    neighbour_candidates = get_connected_neighbour_candidates(location, location_map)
    return {
        candidate
        for candidate in neighbour_candidates
        if location in get_connected_neighbour_candidates(candidate, location_map)
    }


def get_connected_neighbour_candidates(  # noqa: PLR0911
    location: Location, location_map: LocationMap
) -> list[Location]:
    symbol = location_map.get(location, ".")
    row, col = location

    if symbol == ".":
        return []
    elif symbol == "|":
        return [Location(row - 0.5, col), Location(row + 0.5, col)]
    elif symbol == "-":
        return [Location(row, col - 0.5), Location(row, col + 0.5)]
    elif symbol == "L":
        return [Location(row - 0.5, col), Location(row, col + 0.5)]
    elif symbol == "J":
        return [Location(row, col - 0.5), Location(row - 0.5, col)]
    elif symbol == "7":
        return [Location(row, col - 0.5), Location(row + 0.5, col)]
    elif symbol == "F":
        return [Location(row, col + 0.5), Location(row + 0.5, col)]
    elif symbol == "S":
        return [
            # going clockwise, starting at 12
            Location(row - 0.5, col),
            Location(row, col + 0.5),
            Location(row + 0.5, col),
            Location(row, col - 0.5),
        ]
    raise ValueError(f"Unexpected symbol: {symbol}")


def remove_irrelevant_symbols(
    location_map: LocationMap, loop_locations: set[Location]
) -> None:
    for key in location_map.keys():
        if key not in loop_locations:
            location_map[key] = "."


def get_enclosed_locations(
    location_map: LocationMap, loop_locations: set[Location]
) -> set[Location]:
    ...  # TODO


if __name__ == "__main__":
    main("input.txt")
