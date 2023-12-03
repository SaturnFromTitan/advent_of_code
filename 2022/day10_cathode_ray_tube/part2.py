from dataclasses import dataclass, field

from setuptools._vendor.more_itertools import chunked


@dataclass
class Register:
    value: int = 1
    _cycle: int = 0
    outputs: list[str] = field(default_factory=list)

    def noop(self):
        self._increase_cycle()

    def add(self, inc_value):
        self._increase_cycle()
        self._increase_cycle()
        self.value += inc_value

    def _increase_cycle(self):
        self._cycle += 1

        crt_position = (self._cycle - 1) % 40
        if self.value - 1 <= crt_position <= self.value + 1:
            self.outputs.append("#")
        else:
            self.outputs.append(".")


def main():
    with open("input.txt") as f:
        outputs = process_file(f)

    for output_line in chunked(outputs, 40):
        print("".join(output_line))


def process_file(f) -> list[str]:
    register = Register()
    for line in f.readlines():
        line = line.strip()

        if line == "noop":
            register.noop()
        elif line.startswith("addx "):
            value = int(line.replace("addx ", ""))
            register.add(value)
        else:
            raise ValueError(f"Unexpected input: {line}")
    return register.outputs


if __name__ == '__main__':
    main()
