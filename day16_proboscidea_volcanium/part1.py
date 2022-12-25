import itertools
import re
from collections import deque
from dataclasses import dataclass, field


def main():
    with open("input.txt") as f:
        valves = parse_file(f)

    # idea:
    #   1. find the shortest distance between any two valves (using BFS)
    #   2. use BFS or DFS to find the best pressure release strategy:
    #      I.e. an order of valves with flow rate > 0 using the distances
    #      as edge weights.
    shortest_distances = find_shortest_distances(valves)
    answer = release_most_pressure(valves, shortest_distances)
    print(f"THE ANSWER IS: {answer}")


@dataclass(frozen=True)
class Valve:
    id: str
    flow_rate: int
    connected_valves: set[str] = field(default_factory=set)

    def __str__(self):
        return f"Valve '{self.id}'"


ValveMapping = dict[str, Valve]
DistanceMapping = dict[tuple[str, str], int]


@dataclass(frozen=True)
class State:
    current_valve_id: str
    minutes_passed: int = 0
    opened_valves: list[str] = field(default_factory=list)
    released_pressure: int = 0

    _time_limit: int = field(init=False, default=30)

    def minutes_remaining(self) -> int:
        return self._time_limit - self.minutes_passed

    def pressure_release_per_minute(self, valves: ValveMapping) -> int:
        return sum(valves[valve_id].flow_rate for valve_id in self.opened_valves)


def parse_file(f) -> ValveMapping:
    valves: ValveMapping = dict()
    for line in f.readlines():
        line = line.strip()

        pattern = "Valve ([A-Z]+) has flow rate=(\d+); tunnels lead to valves (.+)"
        valve_id, flow_rate, connected_valves = re.match(pattern, line).groups()

        valve = Valve(
            id=valve_id,
            flow_rate=int(flow_rate),
            connected_valves=set(connected_valves.split(", "))
        )
        valves[valve_id] = valve
    return valves


def find_shortest_distances(valves: ValveMapping) -> DistanceMapping:
    return {
        (valve1_id, valve2_id): get_shortest_valve_distance(valve1_id, valve2_id, valves)
        for valve1_id, valve2_id in itertools.permutations(valves.keys(), 2)
    }


def get_shortest_valve_distance(start_id: str, end_id: str, valves: ValveMapping) -> int:
    """Use breath-first search to find the shortest route from start to end"""
    queue = deque([(start_id, 0)])

    while queue:
        valve_id, minutes_passed = queue.popleft()
        valve = valves[valve_id]

        minutes_passed += 1
        for next_valve in valve.connected_valves:
            if next_valve == end_id:
                return minutes_passed

            queue.append((next_valve, minutes_passed))
    raise ValueError("Couldn't find a path connecting the two.")


def release_most_pressure(valves: ValveMapping, shortest_distances: DistanceMapping) -> int:
    relevant_valves = {valve.id for valve in valves.values() if valve.flow_rate > 0}

    start_valve = "AA"
    best = 0
    best_combination: list[str] = list()

    start_state = State(current_valve_id=start_valve)
    queue = deque([start_state])

    i = 0
    while queue:
        i += 1

        state = queue.popleft()
        pressure_release_per_minute = state.pressure_release_per_minute(valves)

        remaining_valves = remaining_reachable_valves(
            state, relevant_valves, shortest_distances
        )

        # no other valves can be opened anymore. there's still time left though
        if not remaining_valves:
            total_pressure_released = state.released_pressure + state.minutes_remaining() * pressure_release_per_minute
            if total_pressure_released > best:
                best = total_pressure_released
                best_combination = [start_valve] + state.opened_valves
            continue

        # open another valve
        for next_valve_id, busy_minutes in remaining_valves:
            pressure_released_while_traveling = busy_minutes * pressure_release_per_minute
            new_state = State(
                current_valve_id=next_valve_id,
                minutes_passed=state.minutes_passed + busy_minutes,
                opened_valves=state.opened_valves.copy() + [next_valve_id],
                released_pressure=state.released_pressure + pressure_released_while_traveling,
            )
            queue.append(new_state)

        # print(state.minutes_passed, len(queue), best)

    times = [get_shortest_valve_distance(v1, v2, valves) for (v1, v2) in itertools.pairwise(best_combination)]
    print(best_combination)
    print(times)
    return best


def remaining_reachable_valves(
    state: State, relevant_valves: set[str], shortest_distances: DistanceMapping
) -> list[tuple[str, int]]:
    remaining_valves = relevant_valves - set(state.opened_valves)

    res: list[tuple[str, int]] = list()
    for next_valve_id in remaining_valves:
        key = (state.current_valve_id, next_valve_id)
        distance = shortest_distances[key]

        # opening the valve itself takes 1 minute as well
        busy_minutes = distance + 1
        if busy_minutes <= state.minutes_remaining():
            res.append((next_valve_id, busy_minutes))
    return res


if __name__ == '__main__':
    main()
