import enum
import itertools
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass

INPUT_FILE = "input.txt"


@enum.unique
class Direction(enum.Enum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


@dataclass(frozen=True)
class Location:
    row: int
    col: int

    def get_neighbour_elves(self, elf_locations) -> set["Location"]:
        neighbours = set()
        for location in self._adjacent_locations():
            if location in elf_locations:
                neighbours.add(location)
        return neighbours

    def north(self):
        return Location(self.row - 1, self.col)

    def north_west(self):
        return Location(self.row - 1, self.col - 1)

    def north_east(self):
        return Location(self.row - 1, self.col + 1)

    def west(self):
        return Location(self.row, self.col - 1)

    def east(self):
        return Location(self.row, self.col + 1)

    def south_east(self):
        return Location(self.row + 1, self.col + 1)

    def south(self):
        return Location(self.row + 1, self.col)

    def south_west(self):
        return Location(self.row + 1, self.col - 1)

    def _adjacent_locations(self) -> Iterator["Location"]:
        yield self.north_west()
        yield self.north()
        yield self.north_east()
        yield self.east()
        yield self.south_east()
        yield self.south()
        yield self.south_west()
        yield self.west()

    def proposals(
        self, start_direction: Direction
    ) -> Iterator[tuple["Location", tuple["Location", "Location"]]]:
        endless_directions = itertools.cycle(Direction)

        # move iterator to start_direction
        start_index = list(Direction).index(start_direction)
        for i in range(start_index):
            next(endless_directions)

        mapping = self._proposal_mapping()
        for _ in range(len(Direction)):
            direction = next(endless_directions)
            yield mapping[direction]

    def _proposal_mapping(
        self
    ) -> dict[Direction, tuple["Location", tuple["Location", "Location"]]]:
        return {
            Direction.NORTH: (self.north(), (self.north_west(), self.north_east())),
            Direction.SOUTH: (self.south(), (self.south_west(), self.south_east())),
            Direction.WEST: (self.west(), (self.north_west(), self.south_west())),
            Direction.EAST: (self.east(), (self.north_east(), self.south_east())),
        }


ElfLocations = set[Location]


def main():
    with open(INPUT_FILE) as f:
        locations = parse_file(f)

    endless_directions = itertools.cycle(Direction)
    for round_num in itertools.count(start=1):
        direction = next(endless_directions)
        new_locations = simulate_round(locations, direction)

        if locations == new_locations:
            break

        locations = new_locations

    print(f"THE ANSWER IS: {round_num}")


def parse_file(f) -> ElfLocations:
    locations: ElfLocations = set()
    for row, line in enumerate(f.readlines()):
        line = line.strip()
        for col, char in enumerate(line):
            if char != "#":
                continue

            locations.add(Location(row=row, col=col))
    return locations


def simulate_round(locations: ElfLocations, direction: Direction) -> ElfLocations:
    # proposals
    proposals: dict[Location, Location] = dict()
    for location in locations:
        neighbours = location.get_neighbour_elves(locations)
        if not neighbours:
            continue

        for proposal, (adjacent1, adjacent2) in location.proposals(direction):
            intersection = {proposal, adjacent1, adjacent2} & neighbours
            if not intersection:
                proposals[location] = proposal
                break

    # move
    proposal_counter = Counter(proposals.values())
    distinct_proposals = {
        proposal for (proposal, count) in proposal_counter.items() if count == 1
    }

    new_locations: ElfLocations = set()
    for original_location in locations:
        if original_location not in proposals:
            new_locations.add(original_location)
            continue

        proposal = proposals[original_location]
        if proposal in distinct_proposals:
            new_locations.add(proposal)
        else:
            new_locations.add(original_location)
    return new_locations


if __name__ == "__main__":
    main()
