import typing
from pathlib import Path

FILE_NAME = Path("input.txt")


class Race(typing.NamedTuple):
    time: int
    distance: int


def main() -> None:
    with open(FILE_NAME) as f:
        race = parse_file(f)

    answer = get_number_of_winning_strategies(race)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> Race:
    lines = list(f.readlines())
    time = int(lines[0].replace("Time:", "").strip().replace(" ", ""))
    distance = int(lines[1].replace("Distance:", "").strip().replace(" ", ""))
    return Race(time, distance)


def get_number_of_winning_strategies(race: Race) -> int:
    num_solutions = 0
    for time_charged in range(1, race.time):
        speed = time_charged
        remaining_time = race.time - time_charged
        distance = speed * remaining_time
        if distance > race.distance:
            num_solutions += 1
        elif num_solutions > 0:
            # this is a convex function
            break
    return num_solutions


if __name__ == "__main__":
    main()
