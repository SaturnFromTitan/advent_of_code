import enum
import sys
import typing

from frozendict import frozendict


class Position(typing.NamedTuple):
    row: int
    col: int


Grid = frozendict[Position, int]


class Direction(enum.StrEnum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP = "UP"
    DOWN = "DOWN"


class State(typing.NamedTuple):
    pos: Position
    direction: Direction | None
    heat: int
    straight_counter: int
    seen: set[tuple[Position, Direction, int]]


def main(file_name: str) -> None:
    with open(file_name) as f:
        grid = parse_file(f)

    answer = find_best_route(grid)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> Grid:
    return frozendict(
        {
            Position(row_index, col_index): int(heat_loss)
            for row_index, row in enumerate(f.read().strip().splitlines())
            for col_index, heat_loss in enumerate(row)
        }
    )


def find_best_route(grid: Grid) -> int:
    start_state = State(
        pos=Position(0, 0), direction=None, heat=0, straight_counter=1, seen=set()
    )
    best_score = sys.maxsize  # a very large int number
    return _find_best_route(grid, start_state, best_score)


def _find_best_route(grid: Grid, state: State, best_score: int) -> int:
    max_row = max([pos.row for pos in grid])
    max_col = max([pos.col for pos in grid])
    target = Position(max_row, max_col)

    for new_position, new_direction, new_straight_counter in get_next_positions(
        state.pos, state.direction, state.straight_counter, max_row, max_col
    ):
        new_state = State(
            pos=new_position,
            direction=new_direction,
            heat=state.heat + grid[new_position],
            straight_counter=new_straight_counter,
            seen=state.seen.copy(),
        )
        if new_state.heat + distance(new_state.pos, target) >= best_score:
            continue

        seen_key = (new_state.pos, new_direction, new_state.straight_counter)
        if seen_key in state.seen:
            continue
        else:
            new_state.seen.add(seen_key)

        if new_position == target:
            print(best_score)
            return min(best_score, new_state.heat)

        best_score = min(best_score, _find_best_route(grid, new_state, best_score))
    return best_score


def get_next_positions(
    pos: Position,
    direction: Direction | None,
    straight_counter: int,
    max_row: int,
    max_col: int,
) -> typing.Iterable[tuple[Position, Direction, int]]:
    for new_direction, new_straight_counter in get_move_candidates(
        direction, straight_counter
    ):
        offset = get_offset(new_direction)
        new_position = Position(pos.row + offset.row, pos.col + offset.col)
        if is_on_grid(new_position, max_row, max_col):
            yield new_position, new_direction, new_straight_counter


def get_move_candidates(
    direction: Direction | None, straight_counter: int
) -> typing.Iterable[tuple[Direction, int]]:
    if direction is None:  # can only happen at start
        yield Direction.RIGHT, straight_counter + 1
        yield Direction.DOWN, straight_counter + 1
    elif direction == Direction.RIGHT:
        if straight_counter < 3:
            yield Direction.RIGHT, straight_counter + 1
        yield Direction.DOWN, 1
        yield Direction.UP, 1
    elif direction == Direction.DOWN:
        if straight_counter < 3:
            yield Direction.DOWN, straight_counter + 1
        yield Direction.RIGHT, 1
        yield Direction.LEFT, 1
    elif direction == Direction.LEFT:
        if straight_counter < 3:
            yield Direction.LEFT, straight_counter + 1
        yield Direction.DOWN, 1
        yield Direction.UP, 1
    else:  # UP
        if straight_counter < 3:
            yield Direction.UP, straight_counter + 1
        yield Direction.RIGHT, 1
        yield Direction.LEFT, 1


def get_offset(direction: Direction) -> Position:
    if direction == Direction.RIGHT:
        return Position(0, 1)
    elif direction == Direction.DOWN:
        return Position(1, 0)
    elif direction == Direction.LEFT:
        return Position(0, -1)
    else:
        return Position(-1, 0)


def is_on_grid(pos: Position, max_row: int, max_col: int) -> bool:
    return 0 <= pos.row <= max_row and 0 <= pos.col <= max_col


def distance(pos: Position, target: Position) -> int:
    return target.row - pos.row + target.col - pos.col


if __name__ == "__main__":
    main("example_input.txt")
