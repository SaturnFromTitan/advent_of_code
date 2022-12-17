import itertools
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Iterator, Optional

Point = namedtuple("Point", ["x", "y"])


@dataclass
class Rock:
    offsets: set[Point]


@dataclass
class Chamber:
    endless_rocks: Iterator[Rock]
    endless_pushes: Iterator[str]
    active_rock: Optional[Rock] = field(init=False, default=None)
    active_rock_anchor: Optional[Point] = field(init=False, default=None)
    width: int = field(default=7, init=False)
    solid_pieces: set[Point] = field(default_factory=set)

    def spawn_new_rock(self):
        self.active_rock = next(self.endless_rocks)
        self.active_rock_anchor = Point(2, self.highest_y() + 2)

    def highest_y(self) -> int:
        return max([point.y for point in self.solid_pieces], default=0)

    def try_shift_active_rock_sideways(self) -> bool:
        direction = next(self.endless_pushes)
        x_shift = -1 if direction == "<" else 1
        return self._shift_active_rock(x_shift, y_shift=0)

    def try_shift_active_rock_down(self) -> bool:
        return self._shift_active_rock(x_shift=0, y_shift=-1)

    def _shift_active_rock(self, x_shift: int, y_shift: int) -> bool:
        anchor = self.active_rock_anchor
        new_anchor = Point(anchor.x + x_shift, anchor.y + y_shift)
        if self._active_rock_can_be_moved(new_anchor):
            self.active_rock_anchor = new_anchor
            return True
        return False

    def _active_rock_can_be_moved(self, new_anchor):
        for offset in self.active_rock.offsets:
            new_point = Point(new_anchor.x + offset.x, new_anchor.y + offset.y)
            if not self._can_be_placed(new_point):
                return False
        return True

    def _can_be_placed(self, point):
        if point.x <= 0:
            # off the board on the left
            return False
        elif point.x > self.width:
            # off the board on the right
            return False
        elif point.y <= 0:
            # through the bottom
            return False
        elif point in self.solid_pieces:
            # collision with solid rock
            return False
        return True

    def make_rock_solid(self):
        anchor = self.active_rock_anchor
        for offset in self.active_rock.offsets:
            point = Point(anchor.x + offset.x, anchor.y + offset.y)
            self.solid_pieces.add(point)
        self._clean_active_rock()

    def _clean_active_rock(self):
        self.active_rock = None
        self.active_rock_anchor = None

    def get_active_rock_points(self):
        if not self.active_rock:
            return set()

        anchor = self.active_rock_anchor
        for offset in self.active_rock.offsets:
            yield Point(anchor.x + offset.x, anchor.y + offset.y)


ROCKS = [
    # -
    Rock(offsets={Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)}),
    # +
    Rock(offsets={Point(1, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(1, 2)}),
    # angle
    Rock(offsets={Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2)}),
    # i
    Rock(offsets={Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)}),
    # block
    Rock(offsets={Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)}),
]


def main():
    with open("example_input.txt") as f:
        pushes = f.read().strip()

    answer = simulate(pushes)
    print(f"THE ANSWER IS: {answer}")


def simulate(pushes) -> int:
    chamber = Chamber(
        endless_rocks=itertools.cycle(ROCKS),
        endless_pushes=itertools.cycle(pushes),
    )

    for _ in range(1):
        chamber.spawn_new_rock()

        while chamber.active_rock:
            chamber.try_shift_active_rock_sideways()
            has_moved = chamber.try_shift_active_rock_down()
            if not has_moved:
                chamber.make_rock_solid()

    visualise(chamber)
    return chamber.highest_y()


def visualise(chamber):
    max_y = chamber.highest_y()
    active_rock_points = set(chamber.get_active_rock_points())

    output = ""
    for y, x in itertools.product(
        range(max_y + 10, -1, -1),
        range(9),
    ):
        point = Point(x, y)

        if point.y == 0:
            output += "-"
        elif point.x in {0, chamber.width + 1}:
            output += "|"
        elif point in chamber.solid_pieces:
            output += "#"
        elif point in active_rock_points:
            output += "@"
        else:
            output += "."

    line_length = chamber.width + 2
    lines = [output[i:i + line_length] for i in range(0, len(output), line_length)]
    for line in lines:
        print(line)


if __name__ == '__main__':
    main()
