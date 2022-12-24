import enum
import itertools
from collections import namedtuple
from dataclasses import dataclass
from functools import lru_cache

Location = namedtuple("Location", ["row", "col"])
State = namedtuple("State", ["location", "minute"])


def main():
    with open("example_input.txt") as f:
        blizzards, start, target = parse_file(f)

    answer = walk_valley(blizzards, start, target)
    print(f"THE ANSWER IS: {answer}")


@enum.unique
class Direction(enum.Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


@dataclass(frozen=True)
class Blizzard:
    id: int
    row: int
    col: int
    direction: Direction

    def get_location(self):
        return Location(self.row, self.col)

    def __str__(self):
        return f"{self.direction.value} at (row={self.row}, col={self.col})"

    def get_next_location(self, max_row, max_col):
        # TODO: save max_row/max_col on the class/instance. they must be identical throughout the run
        #   and therefore shouldn't be parameters here
        min_row, min_col = 1, 1

        # one step in direction
        match self.direction:
            case Direction.UP:
                new_row = self.row - 1
                new_col = self.col
            case Direction.DOWN:
                new_row = self.row + 1
                new_col = self.col
            case Direction.LEFT:
                new_row = self.row
                new_col = self.col - 1
            case Direction.RIGHT:
                new_row = self.row
                new_col = self.col + 1
            case _:
                raise ValueError

        # wrap around
        if new_row < min_row:
            new_row = max_row
        elif new_row > max_row:
            new_row = min_row

        if new_col < min_col:
            new_col = max_col
        elif new_col > max_col:
            new_col = min_col

        return Location(new_row, new_col)


def parse_file(f) -> tuple[tuple[Blizzard, ...], Location, Location]:
    blizzard_ids = itertools.count(start=1)

    blizzards: list[Blizzard] = list()
    for row, line in enumerate(f.readlines()):
        line = line.replace("\n", "")
        for col, char in enumerate(line):
            if char in {"#", "."}:
                continue

            blizzard = Blizzard(
                id=next(blizzard_ids),
                row=row,
                col=col,
                direction=Direction(char),
            )
            blizzards.append(blizzard)

    start = Location(row=0, col=1)
    target = Location(row=row, col=col - 1)
    return tuple(blizzards), start, target


def walk_valley(initial_blizzards: tuple[Blizzard, ...], start: Location, target: Location) -> int:
    # walk valley with depth-first search
    queue = [State(location=start, minute=0)]
    max_blizzard_row = target.row - 1
    max_blizzard_col = target.col
    shortest = float('inf')

    while queue:
        state = queue.pop()
        if state.minute + 1 > shortest:
            continue

        next_blizzards = get_current_blizzards(
            initial_blizzards,
            minute=state.minute + 1,
            max_row=max_blizzard_row,
            max_col=max_blizzard_col
        )
        blizzard_locations = {blizzard.get_location() for blizzard in next_blizzards}

        # new states
        #   positions where I can move/stay
        #   if state.minute + 1 > shortest -> ignore
        for new_location in neighbour_locations(state.location, blizzard_locations):
            if new_location == target:
                shortest = min(shortest, state.minute + 1)
                break

            if (
                new_location.col < 1
                or new_location.col > max_blizzard_col
                or new_location.row < 1
                or new_location.row > max_blizzard_row
            ):
                # out of bounce
                continue

            new_state = State(new_location, minute=state.minute + 1)
            queue.append(new_state)
    return shortest


def neighbour_locations(location, blizzard_locations) -> set[Location]:
    locations = {
        Location(location.row, location.col),  # stay
        Location(location.row - 1, location.col),  # north
        Location(location.row + 1, location.col),  # south
        Location(location.row, location.col - 1),  # west
        Location(location.row, location.col + 1),  # east
    }
    return locations - blizzard_locations


@lru_cache()
def get_current_blizzards(
    initial_blizzards: tuple[Blizzard, ...],
    minute: int,
    max_row: int,
    max_col: int
) -> tuple[Blizzard, ...]:
    """
    recursively calculate blizzard positions, so that it doesn't have to be repeated
    for every state in the simulation.
    """
    if minute == 0:
        return initial_blizzards

    previous_blizzards = get_current_blizzards(
        initial_blizzards,
        minute=minute - 1,
        max_row=max_row,
        max_col=max_col,
    )
    new_blizzards = list()
    for blizzard in previous_blizzards:
        new_location = blizzard.get_next_location(max_row, max_col)
        new_blizzard = Blizzard(
            id=blizzard.id,
            row=new_location.row,
            col=new_location.col,
            direction=blizzard.direction
        )
        new_blizzards.append(new_blizzard)
    return tuple(new_blizzards)


if __name__ == '__main__':
    main()
