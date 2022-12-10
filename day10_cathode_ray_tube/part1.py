from dataclasses import dataclass, field


@dataclass
class Register:
    value: int = 1
    _cycle: int = 0
    signal_strengths: list[int] = field(default_factory=list)

    def noop(self):
        self._increase_cycle()

    def add(self, inc_value):
        self._increase_cycle()
        self._increase_cycle()
        self.value += inc_value

    def _increase_cycle(self):
        self._cycle += 1

        relevant_cycles = {20, 60, 100, 140, 180, 220}
        if self._cycle in relevant_cycles:
            signal_strength = self._cycle * self.value
            self.signal_strengths.append(signal_strength)


def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> int:
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
    return sum(register.signal_strengths)


if __name__ == '__main__':
    main()
