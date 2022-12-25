import itertools
import re
from collections import deque
from dataclasses import dataclass, field

TIME_LIMIT = 30


def main():
    with open("example_input.txt") as f:
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
    opened_valves: set[str] = field(default_factory=set)
    released_pressure: int = 0

    def current_pressure_release(self, valves: ValveMapping):
        summed = 0
        for valve_id in self.opened_valves:
            flow_rate = valves[valve_id].flow_rate
            summed += flow_rate
        return summed


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
    queue = deque([start_id])

    minutes_passed = 0
    while queue:
        valve_id = queue.popleft()
        valve = valves[valve_id]

        minutes_passed += 1
        for next_valve in valve.connected_valves:
            if next_valve == end_id:
                return minutes_passed

            queue.append(next_valve)
    raise ValueError("Couldn't find a path connecting the two.")


def release_most_pressure(valves: ValveMapping, shortest_distances: DistanceMapping) -> int:
    """
    Use DFS to find the best strategy to open the valves.

    Using DFS instead of BFS because we need to explore the full search space anyways. With
    DFS we can terminate some paths
    """
    relevant_valves = {valve.id for valve in valves.values() if valve.flow_rate > 0}

    best = 0

    start_state = State(current_valve_id="AA")
    queue = [start_state]
    while queue:
        state = queue.pop()
        pressure_release_this_round = state.current_pressure_release(valves)
        remaining_minutes = TIME_LIMIT - state.minutes_passed

        # time's up
        if not remaining_minutes:
            best = max(best, state.released_pressure)
            continue

        remaining_valves = relevant_valves - state.opened_valves

        # open another valve
        other_valves_reachable = False
        for next_valve_id in remaining_valves:
            key = (state.current_valve_id, next_valve_id)
            distance = shortest_distances[key]
            if distance > remaining_minutes:
                # valve not reachable in time
                continue

            extra_pressure_release_while_traveling = distance * pressure_release_this_round
            new_state = State(
                current_valve_id=next_valve_id,
                minutes_passed=state.minutes_passed + distance,
                opened_valves=state.opened_valves | {next_valve_id},
                released_pressure=state.released_pressure + extra_pressure_release_while_traveling,
            )
            queue.append(new_state)
            other_valves_reachable = True

        # no other valves can be opened anymore. there's still time left though
        if not other_valves_reachable:
            total_pressure_released = state.released_pressure + remaining_minutes * pressure_release_this_round
            best = max(best, total_pressure_released)
            continue
    return best


if __name__ == '__main__':
    main()
