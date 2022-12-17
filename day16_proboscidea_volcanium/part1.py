import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Room:
    valve: str
    flow_rate: int
    connected_valves: list[str] = field(default_factory=list)

    def __str__(self):
        return f"Valve {self.valve}"


def main():
    with open("input.txt") as f:
        rooms = parse_file(f)

    answer = release_pressure(rooms)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f):
    rooms = dict()
    for line in f.readlines():
        line = line.strip()

        pattern = "Valve ([A-Z]+) has flow rate=(\d+); tunnels lead to valves (.+)"
        valve, flow_rate, connected_valves = re.match(pattern, line).groups()
        room = Room(valve=valve, flow_rate=int(flow_rate), connected_valves=connected_valves.split(", "))
        rooms[valve] = room
    return rooms


def release_pressure(rooms):
    current_valve = "VN"
    opened_valves = set()
    visited_valves = set()

    released = 0
    active_flow_rate_per_minute = 0
    for i in range(30):
        released += active_flow_rate_per_minute

        # open valve
        flow_rate = flow_rates[current_valve]
        if current_valve not in opened_valves and flow_rate > 0:
            opened_valves.add(current_valve)
            active_flow_rate_per_minute += flow_rate
            continue

        # visited rooms
        visited_valves
    return released


if __name__ == '__main__':
    main()
