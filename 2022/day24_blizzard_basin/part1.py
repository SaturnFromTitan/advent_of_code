import enum
import itertools
from collections import deque, namedtuple
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache

Location = namedtuple("Location", ["row", "col"])
State = namedtuple("State", ["location", "minute"])


def main():
    blizzards, start, target = parse_file("input.txt")

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

    max_row: int
    max_col: int
    min_row: int = 1
    min_col: int = 1

    def get_location(self):
        return Location(self.row, self.col)

    def __str__(self):
        return f"{self.direction.value} at (row={self.row}, col={self.col})"

    def get_next_location(self):
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
        if new_row < self.min_row:
            new_row = self.max_row
        elif new_row > self.max_row:
            new_row = self.min_row

        if new_col < self.min_col:
            new_col = self.max_col
        elif new_col > self.max_col:
            new_col = self.min_col

        return Location(new_row, new_col)


def parse_file(file_name) -> tuple[tuple[Blizzard, ...], Location, Location]:
    with open(file_name) as f:
        max_blizzard_row, max_blizzard_col = _parse_dimensions(f)

    with open(file_name) as f:
        blizzards = _parse_blizzards(f, max_blizzard_row, max_blizzard_col)

    start = Location(row=0, col=1)
    target = Location(row=max_blizzard_row + 1, col=max_blizzard_col)
    return blizzards, start, target


def _parse_blizzards(
    f, max_blizzard_row: int, max_blizzard_col: int
) -> tuple[Blizzard, ...]:
    blizzard_ids = itertools.count(start=1)

    blizzards: list[Blizzard] = list()
    for row, line in enumerate(f.readlines()):
        for col, char in enumerate(line.strip()):
            if char in {"#", "."}:
                continue

            blizzard = Blizzard(
                id=next(blizzard_ids),
                row=row,
                col=col,
                direction=Direction(char),
                max_row=max_blizzard_row,
                max_col=max_blizzard_col,
            )
            blizzards.append(blizzard)
    return tuple(blizzards)


def _parse_dimensions(f):
    lines = f.readlines()
    line = lines[0].strip()
    return len(lines) - 2, len(line) - 2


def walk_valley(
    initial_blizzards: tuple[Blizzard, ...], start: Location, target: Location
) -> int:
    # walk valley with depth-first search
    queue = deque([State(location=start, minute=0)])
    seen: set[tuple[Location, tuple[Blizzard, ...]]] = set()

    max_blizzard_row = target.row - 1
    max_blizzard_col = target.col

    i = 0
    while queue:
        i += 1

        state = queue.popleft()
        next_minute = state.minute + 1

        next_blizzards = get_current_blizzards(
            initial_blizzards,
            minute=next_minute,
        )
        blizzard_locations = {blizzard.get_location() for blizzard in next_blizzards}

        # new states
        for new_location in neighbour_locations(state.location, blizzard_locations):
            if new_location == target:
                return next_minute

            if state.location != start and new_location == start:
                # disallow moving back to the start
                # the same can be achieved by staying at the start from the beginning on,
                # so this is a redundant strategy
                continue

            out_of_valley = (
                new_location.row < 1
                or new_location.row > max_blizzard_row
                or new_location.col < 1
                or new_location.col > max_blizzard_col
            )
            if out_of_valley and new_location != start:
                continue

            key = (new_location, next_blizzards)
            if key in seen:
                continue
            seen.add(key)

            new_state = State(new_location, minute=next_minute)
            queue.append(new_state)

        if i % 500 == 0:
            print(state.minute, len(queue))
    raise ValueError("Couldn't find a route through the valley")


def neighbour_locations(location, blizzard_locations) -> Iterator[Location]:
    # put the most relevant directions in the bottom, since we use depth-first search
    # -> that means these will be used first
    locations = [
        Location(location.row, location.col),  # stay
        Location(location.row, location.col - 1),  # west
        Location(location.row - 1, location.col),  # north
        Location(location.row, location.col + 1),  # east
        Location(location.row + 1, location.col),  # south
    ]
    return (loc for loc in locations if loc not in blizzard_locations)


@cache
def get_current_blizzards(
    initial_blizzards: tuple[Blizzard, ...],
    minute: int,
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
    )
    new_blizzards = list()
    for blizzard in previous_blizzards:
        new_location = blizzard.get_next_location()
        new_blizzard = Blizzard(
            id=blizzard.id,
            row=new_location.row,
            col=new_location.col,
            direction=blizzard.direction,
            max_row=blizzard.max_row,
            max_col=blizzard.max_col,
        )
        new_blizzards.append(new_blizzard)
    return tuple(new_blizzards)


if __name__ == "__main__":
    main()
