import typing
from pathlib import Path

FILE_NAME = Path("input.txt")


class Position(typing.NamedTuple):
    row: int
    col: int


class Number(typing.NamedTuple):
    id: int
    value: int


NumberPositions = dict[Position, Number]
NumberMapping = dict[int, Number]
SymbolPositions = list[Position]


def main() -> None:
    with open(FILE_NAME) as f:
        number_positions, gear_positions = parse_file(f)

    answer = get_gear_ratio_sum(number_positions, gear_positions)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> tuple[NumberPositions, SymbolPositions]:
    number_str = ""
    number_positions_temp: list[Position] = []
    number_positions = {}
    gear_positions = []
    number_id = 0
    for row_index, line_raw in enumerate(f.readlines()):
        line = line_raw.strip()
        for col_index, char in enumerate(line):
            # col_index == 0 check as a number can also end on line-breaks
            if number_str and (not char.isdigit() or (col_index == 0)):
                number = Number(id=number_id, value=int(number_str))
                for position_temp in number_positions_temp:
                    number_positions[position_temp] = number
                number_str = ""
                number_positions_temp = []
                number_id += 1

            if char.isdigit():
                number_str += char
                number_positions_temp.append(Position(row_index, col_index))
            elif char == "*":
                gear_positions.append(Position(row_index, col_index))

    if number_str:
        # not needed with my data - so for simplicity it's skipped
        msg = "data ends with a number that still needs to be added to the mappings"
        raise ValueError(msg)
    return number_positions, gear_positions


def get_gear_ratio_sum(
    number_positions: NumberPositions, gear_positions: SymbolPositions
) -> int:
    return sum(
        get_gear_ratio(symbol_position, number_positions)
        for symbol_position in gear_positions
    )


def get_gear_ratio(symbol_position: Position, number_positions: NumberPositions) -> int:
    adjacent_numbers = set()
    for position in get_adjacent_positions(symbol_position):
        number = number_positions.get(position)
        if number:
            adjacent_numbers.add(number)

    if len(adjacent_numbers) != 2:
        return 0

    first_number, second_number = list(adjacent_numbers)
    return first_number.value * second_number.value


def get_adjacent_positions(position: Position) -> typing.Iterable[Position]:
    # going clockwise, starting at 12
    yield Position(position.row - 1, position.col)
    yield Position(position.row - 1, position.col + 1)
    yield Position(position.row, position.col + 1)
    yield Position(position.row + 1, position.col + 1)
    yield Position(position.row + 1, position.col)
    yield Position(position.row + 1, position.col - 1)
    yield Position(position.row, position.col - 1)
    yield Position(position.row - 1, position.col - 1)


if __name__ == "__main__":
    main()
