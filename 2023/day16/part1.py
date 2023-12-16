import enum


class Direction(enum.StrEnum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP = "UP"
    DOWN = "DOWN"


RayPosition = tuple[int, int, Direction]


def main(file_name: str) -> None:
    with open(file_name) as f:
        grid = parse_file(f)

    answer = simulate_sunray(grid)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> list[str]:
    return f.read().strip().splitlines()


def simulate_sunray(grid: list[str]) -> int:
    current_ray_positions = {(0, -1, Direction.RIGHT)}
    ray_positions = current_ray_positions.copy()
    previous_ray_positions: set[RayPosition] = set()
    while ray_positions != previous_ray_positions:
        previous_ray_positions = ray_positions.copy()
        current_ray_positions = move_ray(current_ray_positions, grid)
        ray_positions |= current_ray_positions
    activated_tiles = {(row, col) for (row, col, _) in ray_positions} - {(0, -1)}
    return len(activated_tiles)


def move_ray(ray_positions: set[RayPosition], grid: list[str]) -> set[RayPosition]:
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1

    new_ray_positions = set()
    for pos in ray_positions:
        row, col, _ = pos
        symbol = grid[row][col]
        new_ray_positions |= get_new_positions(symbol, pos, max_row, max_col)
    return new_ray_positions


def get_new_positions(
    symbol: str, position: RayPosition, max_row: int, max_col: int
) -> set[RayPosition]:
    row, col, direction = position
    match (direction, symbol):
        # RIGHT
        case (Direction.RIGHT, "."):
            offsets = {(0, 1, Direction.RIGHT)}
        case (Direction.RIGHT, "-"):
            offsets = {(0, 1, Direction.RIGHT)}
        case (Direction.RIGHT, "|"):
            offsets = {(-1, 0, Direction.UP), (1, 0, Direction.DOWN)}
        case (Direction.RIGHT, "/"):
            offsets = {(-1, 0, Direction.UP)}
        case (Direction.RIGHT, "\\"):
            offsets = {(1, 0, Direction.DOWN)}
        # LEFT
        case (Direction.LEFT, "."):
            offsets = {(0, -1, Direction.LEFT)}
        case (Direction.LEFT, "-"):
            offsets = {(0, -1, Direction.LEFT)}
        case (Direction.LEFT, "|"):
            offsets = {(-1, 0, Direction.UP), (1, 0, Direction.DOWN)}
        case (Direction.LEFT, "/"):
            offsets = {(1, 0, Direction.DOWN)}
        case (Direction.LEFT, "\\"):
            offsets = {(-1, 0, Direction.UP)}
        # UP
        case (Direction.UP, "."):
            offsets = {(-1, 0, Direction.UP)}
        case (Direction.UP, "-"):
            offsets = {(0, -1, Direction.LEFT), (0, 1, Direction.RIGHT)}
        case (Direction.UP, "|"):
            offsets = {(-1, 0, Direction.UP)}
        case (Direction.UP, "/"):
            offsets = {(0, 1, Direction.RIGHT)}
        case (Direction.UP, "\\"):
            offsets = {(0, -1, Direction.LEFT)}
        # DOWN
        case (Direction.DOWN, "."):
            offsets = {(1, 0, Direction.DOWN)}
        case (Direction.DOWN, "-"):
            offsets = {(0, -1, Direction.LEFT), (0, 1, Direction.RIGHT)}
        case (Direction.DOWN, "|"):
            offsets = {(1, 0, Direction.DOWN)}
        case (Direction.DOWN, "/"):
            offsets = {(0, -1, Direction.LEFT)}
        case (Direction.DOWN, "\\"):
            offsets = {(0, 1, Direction.RIGHT)}
        case _:
            raise ValueError("Can't map this direction & symbol")

    return {
        (row + row_offset, col + col_offset, new_direction)
        for (row_offset, col_offset, new_direction) in offsets
        if 0 <= row + row_offset <= max_row and 0 <= col + col_offset <= max_col
    }


if __name__ == "__main__":
    main("input.txt")
