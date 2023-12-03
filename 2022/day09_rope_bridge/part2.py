from dataclasses import dataclass


class Rope:
    def __init__(self, number_of_knots):
        self.knots = tuple(Knot() for _ in range(number_of_knots))

    def move_one_step(self, direction):
        previous_knot = None
        for knot in self.knots:
            if not previous_knot:
                knot.move(direction)
            else:
                knot.follow(previous_knot)
            previous_knot = knot

    def get_locations(self):
        return [k.get_location() for k in self.knots]


@dataclass
class Knot:
    x: int = 0
    y: int = 0

    def move(self, direction):
        if direction == "R":
            self.x += 1
        elif direction == "L":
            self.x -= 1
        elif direction == "U":
            self.y += 1
        elif direction == "D":
            self.y -= 1
        else:
            raise ValueError(f"Receive unexpected direction '{direction}'")

    def follow(self, other: "Knot"):
        delta_y = other.y - self.y
        delta_x = other.x - self.x
        if abs(delta_y) > 1 or abs(delta_x) > 1:
            self.x += self.sign(delta_x)
            self.y += self.sign(delta_y)

    @staticmethod
    def sign(num: int):
        return int(num > 0) - int(num < 0)

    def get_location(self):
        return self.x, self.y


def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> int:
    rope = Rope(number_of_knots=10)

    tail_locations = set()
    for idx, line in enumerate(f.readlines()):
        direction, amount = line.split()

        for _ in range(int(amount)):
            rope.move_one_step(direction)
            tail = rope.knots[-1]
            tail_locations.add(tail.get_location())
    return len(tail_locations)


if __name__ == "__main__":
    main()
