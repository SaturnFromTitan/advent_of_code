import collections
import enum
import functools
import sys
import time
import typing

from frozendict import frozendict


class Position(typing.NamedTuple):
    row: int
    col: int


Grid = frozendict[Position, int]


class Direction(enum.StrEnum):
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    UP = "UP"
    LEFT = "LEFT"


class State(typing.NamedTuple):
    pos: Position
    direction: Direction
    straight_counter: int

    def __str__(self):
        return f"State(pos=({self.pos.row}, {self.pos.col}), direction={self.direction}, straight_counter={self.straight_counter})"


class heat_cache:
    """Similar to `functools.cache`, but using a custom cache key"""

    def __init__(self):
        self.cache: dict = {}

    def __call__(self, func: typing.Callable) -> typing.Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key: State = kwargs["start_state"]
            if key in self.cache:
                return self.cache[key]

            result = func(*args, **kwargs)
            self.cache[key] = result
            return result

        return wrapper


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
    max_row = max([pos.row for pos in grid])
    max_col = max([pos.col for pos in grid])
    assert max_row == max_col, "assuming quadratic grid..."
    target = Position(max_row, max_col)

    relevant_scores = []
    for dist in range(max_row + 1):
        for row_offset in range(dist + 1):
            for col_offset in range(dist + 1):
                new_pos = Position(target.row - row_offset, target.col - col_offset)
                print(f"Finding best score from {new_pos}")
                for _direction in Direction:
                    direction = Direction(_direction)  # so that mypy isn't confused
                    direction_solution = (
                        sys.maxsize,
                        (direction, direction, direction),
                    )

                    for straight_count in range(1, 4):
                        temp_start_state = State(
                            pos=new_pos,
                            direction=direction,
                            straight_counter=straight_count,
                        )
                        # the result is cached and can be reused by the next iteration
                        if (
                            get_num_moves_in_direction_at_start(
                                direction_solution[1], direction
                            )
                            < straight_count
                        ):
                            solution = direction_solution
                        else:
                            solution = None
                        score, moves = _find_best_route(
                            grid=grid,
                            start_state=temp_start_state,
                            solution=solution,
                        )
                        print(f"\tscore: {score}")
                        if score < direction_solution[0]:
                            direction_solution = (score, moves)

                        if (
                            row_offset == max_row
                            and col_offset == max_col
                            and straight_count == 1
                        ):
                            relevant_scores.append(score)
    return min(relevant_scores)


@heat_cache()  # type: ignore[no-untyped-call]
def _find_best_route(
    grid: Grid, start_state: State, solution: None | tuple[int, tuple[Direction, ...]]
) -> tuple[int, tuple[Direction, ...]]:
    if solution:
        return solution

    print(f"\tFinding best route for {start_state}")

    max_row = max([pos.row for pos in grid])
    max_col = max([pos.col for pos in grid])
    target = Position(max_row, max_col)

    best_score = sys.maxsize  # a very large integer
    best_moves: tuple[Direction, ...] = ()

    queue: collections.deque[
        tuple[State, int, tuple[Direction, ...]]
    ] = collections.deque([(start_state, 0, ())])
    while queue:
        state, current_score, moves = queue.popleft()
        new_score = current_score + grid[state.pos]
        new_moves = (*moves, state.direction)
        if state.pos == target and new_score < best_score:
            best_score = new_score
            best_moves = new_moves

        for new_state in get_next_positions_sorted(state):
            if (
                not is_on_grid(new_state.pos, max_row, max_col)
                or new_score + grid[new_state.pos] + distance(new_state.pos, target) - 1
                >= best_score
            ):
                continue

            queue.appendleft((new_state, new_score, new_moves))
    assert best_score < sys.maxsize, f"Didn't find a route from {start_state.pos}"
    return best_score, best_moves


def get_next_positions_sorted(state: State) -> list[State]:
    # reverse as _find_best_route uses .appendleft for all directions
    # -> the order here is reversed again
    # FYI: I tried sorting by grid[new_state.pos] as well, but it doesn't converge well
    return list(get_next_positions(state))[::-1]


def get_next_positions(state: State) -> typing.Iterable[State]:
    for new_direction, new_straight_counter in get_move_candidates(
        state.direction, state.straight_counter
    ):
        offset = get_offset(new_direction)
        new_position = Position(state.pos.row + offset.row, state.pos.col + offset.col)
        yield State(new_position, new_direction, new_straight_counter)


def get_move_candidates(
    direction: Direction, straight_counter: int
) -> typing.Iterable[tuple[Direction, int]]:
    if direction == Direction.RIGHT:
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


def get_num_moves_in_direction_at_start(
    moves: tuple[Direction, ...], direction: Direction
) -> int:
    moved_straight = 0
    for move in moves:
        if move == direction:
            moved_straight += 1
        else:
            break

    if moved_straight > 3:
        raise ValueError(f"Moved too long in one direction...\n\t{moves}")
    return moved_straight


if __name__ == "__main__":
    start = time.monotonic()
    main("example_input.txt")
    print("time elapsed:", round(time.monotonic() - start, 1), "seconds")
