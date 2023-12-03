from dataclasses import dataclass


@dataclass
class Rope:
    head_x: int = 0
    head_y: int = 0

    tail_x: int = 0
    tail_y: int = 0

    def move_one_step(self, direction):
        self._move_head(direction)
        self._pull_tail()

    def _move_head(self, direction):
        if direction == "R":
            self.head_x += 1
        elif direction == "L":
            self.head_x -= 1
        elif direction == "U":
            self.head_y += 1
        elif direction == "D":
            self.head_y -= 1
        else:
            raise ValueError(f"Receive unexpected direction '{direction}'")

    def _pull_tail(self):
        delta_y = self.head_y - self.tail_y
        delta_x = self.head_x - self.tail_x
        if abs(delta_y) <= 1 and abs(delta_x) <= 1:
            # head & tail are still touching
            return

        # follow vertically
        if delta_x == 0:
            if delta_y > 0:
                self.tail_y += 1
            elif delta_y < 0:
                self.tail_y -= 1
            return

        # follow horizontally
        if delta_y == 0:
            if delta_x > 0:
                self.tail_x += 1
            elif delta_x < 0:
                self.tail_x -= 1
            return

        # follow diagonally
        if delta_x > 0 and delta_y > 0:
            self.tail_x += 1
            self.tail_y += 1
        elif delta_x > 0 and delta_y < 0:
            self.tail_x += 1
            self.tail_y -= 1
        elif delta_x < 0 and delta_y < 0:
            self.tail_x -= 1
            self.tail_y -= 1
        elif delta_x < 0 and delta_y > 0:
            self.tail_x -= 1
            self.tail_y += 1

    def get_tail_location(self):
        return self.tail_x, self.tail_y


def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> int:
    rope = Rope()

    tail_locations = set()
    for line in f.readlines():
        direction, amount = line.split()

        for _ in range(int(amount)):
            rope.move_one_step(direction)
            tail_locations.add(rope.get_tail_location())
    return len(tail_locations)


if __name__ == "__main__":
    main()
