import enum

FILE_NAME = "input.txt"


@enum.unique
class Action(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


@enum.unique
class Result(enum.Enum):
    WIN = 6
    DRAW = 3
    LOSS = 0


def main():
    with open(FILE_NAME) as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f):
    total = 0

    for line in f.readlines():
        opponent_char, my_char = line.split()
        opponent_action = translate_input(opponent_char)
        my_action = translate_input(my_char)

        result = determine_winner(opponent_action, my_action)

        total += result.value + my_action.value
    return total


def determine_winner(opponent_action, my_action):
    if opponent_action == my_action:
        return Result.DRAW

    if (
        opponent_action == Action.ROCK and my_action == Action.PAPER
        or opponent_action == Action.PAPER and my_action == Action.SCISSORS
        or opponent_action == Action.SCISSORS and my_action == Action.ROCK
    ):
        return Result.WIN
    return Result.LOSS


def translate_input(char):
    if char in {"A", "X"}:
        return Action.ROCK
    elif char in {"B", "Y"}:
        return Action.PAPER
    elif char in {"C", "Z"}:
        return Action.SCISSORS
    raise ValueError(f"Received unexpected character '{char}'")


if __name__ == '__main__':
    main()
