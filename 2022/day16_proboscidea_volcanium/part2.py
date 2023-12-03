"""
Idea, inspired by this reddit post:
https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0xbg57/?utm_source=share&utm_medium=web2x&context=3

Run the simulation from part1, but store all possible (sub) "paths" for 26 minutes and the
total pressure they would release. I.e. also include paths that only open 0, 1, etc. valves.
I.e. something like:

paths = {
    (): 0,
    ("DD"): 500,
    ("DD", "JJ"): 1400,
    ...
}

Now for every sub path, find all other *distinct* sub paths and add their pressure releases.

The maximum of these sums is the result.

UPDATE: The number of all sub-paths is so big that computing all combinations among them is
    too heavy. Therefore we first search for the best permutation of the nodes in the sub-path
    beforehand.
"""

import itertools
import re
from collections import deque
from dataclasses import dataclass, field


def main():
    with open("input.txt") as f:
        valves = parse_file(f)

    shortest_distances = find_shortest_distances(valves)
    sub_path_pressures = find_best_pressure_release_for_sub_paths(
        valves, shortest_distances
    )
    sub_path_pressures_ordered = find_best_permutation_of_sub_paths(sub_path_pressures)
    answer = find_best_combinations(sub_path_pressures_ordered)
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

    _time_limit: int = field(init=False, default=26)

    def minutes_remaining(self) -> int:
        return self._time_limit - self.minutes_passed

    def pressure_release_per_minute(self, valves: ValveMapping) -> int:
        return sum(valves[valve_id].flow_rate for valve_id in self.opened_valves)


def parse_file(f) -> ValveMapping:
    valves: ValveMapping = dict()
    for line in f.readlines():
        line = line.strip()

        pattern = r"Valve ([A-Z]+) has flow rate=(\d+); tunnels lead to valves (.+)"
        valve_id, flow_rate, connected_valves = re.match(pattern, line).groups()

        valve = Valve(
            id=valve_id,
            flow_rate=int(flow_rate),
            connected_valves=set(connected_valves.split(", ")),
        )
        valves[valve_id] = valve
    return valves


def find_shortest_distances(valves: ValveMapping) -> DistanceMapping:
    return {
        (valve1_id, valve2_id): get_shortest_valve_distance(
            valve1_id, valve2_id, valves
        )
        for valve1_id, valve2_id in itertools.permutations(valves.keys(), 2)
    }


def get_shortest_valve_distance(
    start_id: str, end_id: str, valves: ValveMapping
) -> int:
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
    raise ValueError(f"Couldn't find a path connecting '{start_id}' and '{end_id}'.")


def find_best_pressure_release_for_sub_paths(
    valves: ValveMapping, shortest_distances: DistanceMapping
) -> dict[tuple[str, ...], int]:
    relevant_valves = {valve.id for valve in valves.values() if valve.flow_rate > 0}

    start_state = State(current_valve_id="AA")
    queue = deque([start_state])

    bests: dict[tuple[str, ...], int] = dict()
    while queue:
        state = queue.popleft()
        pressure_release_per_minute = state.pressure_release_per_minute(valves)

        remaining_valves = remaining_reachable_valves(
            state, relevant_valves, shortest_distances
        )

        # open another valve
        for next_valve_id, busy_minutes in remaining_valves:
            pressure_released_while_traveling = (
                busy_minutes * pressure_release_per_minute
            )
            new_state = State(
                current_valve_id=next_valve_id,
                minutes_passed=state.minutes_passed + busy_minutes,
                opened_valves=state.opened_valves + [next_valve_id],
                released_pressure=state.released_pressure
                + pressure_released_while_traveling,
            )
            queue.append(new_state)

        # also simulate that no other valve is being opened
        total_pressure_released = (
            state.released_pressure
            + state.minutes_remaining() * pressure_release_per_minute
        )
        bests[tuple(state.opened_valves)] = total_pressure_released
    return bests


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


def find_best_permutation_of_sub_paths(
    sub_path_pressures: dict[tuple[str, ...], int]
) -> dict[frozenset[str, ...], int]:
    bests: dict[frozenset[str, ...], int] = dict()
    for sub_path, pressure in sub_path_pressures.items():
        key = frozenset(sub_path)
        bests[key] = max(bests.get(key, 0), pressure)
    return bests


def find_best_combinations(sub_path_pressures: dict[frozenset[str, ...], int]) -> int:
    best = 0

    print(len(sub_path_pressures))
    combinations = itertools.combinations(sub_path_pressures.items(), 2)
    for (sub_path1, pressure1), (sub_path2, pressure2) in combinations:
        intersection = sub_path1 & sub_path2
        # it's inefficient if both "players" go to the same valve, so we can ignore this
        if intersection:
            continue

        score = pressure1 + pressure2
        best = max(best, score)
    return best


if __name__ == "__main__":
    main()
