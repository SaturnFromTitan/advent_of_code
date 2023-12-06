import math
import typing
from pathlib import Path

FILE_NAME = Path("example_input.txt")


class Race(typing.NamedTuple):
    time: int
    distance: int


def main() -> None:
    with open(FILE_NAME) as f:
        races = parse_file(f)

    answer = math.prod([get_number_of_winning_strategies(race) for race in races])
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> list[Race]:
    lines = list(f.readlines())
    times = [int(val) for val in lines[0].replace("Time:", "").strip().split()]
    distances = [int(val) for val in lines[1].replace("Distance:", "").strip().split()]
    return [
        Race(time, distance) for (time, distance) in zip(times, distances, strict=True)
    ]


def get_number_of_winning_strategies(race: Race) -> int:
    num_solutions = 0
    for time_charged in range(1, race.time):
        speed = time_charged
        remaining_time = race.time - time_charged
        distance = speed * remaining_time
        if distance > race.distance:
            num_solutions += 1
    return num_solutions


if __name__ == "__main__":
    main()
