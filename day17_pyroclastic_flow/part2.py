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
    max_y: int = field(default=0, init=False)

    def spawn_new_rock(self):
        self.active_rock = next(self.endless_rocks)
        self.active_rock_anchor = Point(3, self.max_y + 4)

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
        active_rock_points = list(self.get_active_rock_points())
        self.solid_pieces.update(active_rock_points)

        # update max_y
        max_y_of_new_rock = max([point.y for point in active_rock_points], default=0)
        self.max_y = max(self.max_y, max_y_of_new_rock)

        # remove active rock
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
    with open("input.txt") as f:
        pushes = f.read().strip()
    num_pushes = len(pushes)

    # answer = simulate(pushes)
    # print(f"THE ANSWER IS: {answer}")
    # raise SystemExit

    # The row is completely filled periodically again. Based on some trials (that can be
    # seen in the extra prints in the 'simulate' function) I found that after an initial
    # offset of 216 rocks / y = 325, the height difference is identical after alternating
    # 1130 & 585 rocks (and 1750 & 863 height). With that I can compute the height after
    # 10^12 rocks:
    offset_rocks = 216
    offset_height = 325
    period_rocks = 1130 + 585  # 1715
    period_height = 1750 + 863  # 2613

    target_rocks = 10 ** 12
    full_cycles = (target_rocks - offset_rocks) // period_rocks

    # after offset_height + full_cycles * period_height rocks there's
    # a remainder smaller than period_rocks. It can be calculated via
    #
    # remainder_rocks = (target_rocks - offset_rocks) % period_rocks
    # print(remainder_rocks)
    # push_offset = (target_rocks - remainder_rocks) % num_pushes
    # print("PUSH OFFSET", push_offset)
    # raise SystemExit
    #
    # With the simulate function we can derive how much height these
    # extra rocks represent:
    remainder_height = 2306

    answer = offset_height + (full_cycles * period_height) + remainder_height
    print(f"THE ANSWER IS: {answer}")

    # The answer is WRONG. I think the problem is that I need to take the
    # wind push offsets into account as well. Also the rock_offset isn't
    # divisible by 5, so that probably causes trouble as well.
    #
    # to be continued...


def simulate(pushes) -> int:
    endless_rocks = itertools.cycle(ROCKS)
    next(endless_rocks)

    endless_pushes = itertools.cycle(pushes)
    for i in range(8867):
        next(endless_pushes)

    chamber = Chamber(
        endless_rocks=itertools.cycle(ROCKS),
        endless_pushes=endless_pushes,
    )
    prev__row_filled = 0
    prev__height = 0
    for rock_counter in range(314):
        is_row_filled = all(
            Point(x, chamber.max_y) in chamber.solid_pieces
            for x in range(1, chamber.width + 1)
        )
        if is_row_filled:
            diff__counter = rock_counter - prev__row_filled
            print("ROCK COUNTER", rock_counter, "--- DIFF ---", diff__counter)
            diff__height = chamber.max_y - prev__height
            print("HEIGHT", chamber.max_y, "--- DIFF ---", diff__height)
            print("*" * 50)
            prev__row_filled = rock_counter
            prev__height = chamber.max_y
        chamber.spawn_new_rock()

        while chamber.active_rock:
            chamber.try_shift_active_rock_sideways()
            has_moved = chamber.try_shift_active_rock_down()
            if not has_moved:
                chamber.make_rock_solid()
    return chamber.max_y


def visualise(chamber):
    active_rock_points = set(chamber.get_active_rock_points())

    output = ""
    for y, x in itertools.product(
        range(chamber.max_y + 10, -1, -1),
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
