from pathlib import Path

file_name = Path("input.txt")

COLOUR_LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def main() -> None:
    with open(file_name) as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f) -> int:
    summed = 0
    for line in f.readlines():
        game_id_part, game_info = line.split(": ")
        if not is_possible(game_info):
            continue

        game_id = int(game_id_part.replace("Game ", "").strip())
        summed += game_id
    return summed


def is_possible(game_info: str) -> bool:
    for game_draw in game_info.split("; "):
        for cube_draw in game_draw.split(", "):
            for colour, limit in COLOUR_LIMITS.items():
                try:
                    num = int(cube_draw.replace(colour, "").strip())
                except ValueError:
                    continue

                if num > limit:
                    return False
    return True


if __name__ == "__main__":
    main()
