import functools
from pathlib import Path

file_name = Path("input.txt")

COLOURS = [
    "red",
    "green",
    "blue",
]


def main() -> None:
    with open(file_name) as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> int:
    summed = 0
    for line in f.readlines():
        game_id_part, game_info = line.split(": ")
        summed += get_power(game_info)
    return summed


def get_power(game_info: str) -> int:
    min_cube_counts = dict.fromkeys(COLOURS, 0)
    for game_draw in game_info.split("; "):
        for cube_draw in game_draw.split(", "):
            for colour in COLOURS:
                try:
                    cube_count = int(cube_draw.replace(colour, "").strip())
                except ValueError:
                    continue

                min_cube_counts[colour] = max(min_cube_counts[colour], cube_count)
    print(min_cube_counts)
    power = functools.reduce(lambda x, y: x * y, min_cube_counts.values())
    print(power)
    return power


if __name__ == "__main__":
    main()
