import enum

FILE_NAME = "input.txt"


@enum.unique
class Action(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


WEAKNESSES = {
    Action.ROCK: Action.PAPER,
    Action.PAPER: Action.SCISSORS,
    Action.SCISSORS: Action.ROCK,
}
STRENGTHS = {v: k for (k, v) in WEAKNESSES.items()}


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
        result = translate_instruction(my_char)

        my_action = choose_my_action(opponent_action, result)

        total += result.value + my_action.value
    return total


def translate_input(char):
    if char == "A":
        return Action.ROCK
    elif char == "B":
        return Action.PAPER
    elif char == "C":
        return Action.SCISSORS
    raise ValueError(f"Received unexpected character '{char}'")


def translate_instruction(char):
    if char == "X":
        return Result.LOSS
    elif char == "Y":
        return Result.DRAW
    elif char == "Z":
        return Result.WIN
    raise ValueError(f"Received unexpected character '{char}'")


def choose_my_action(opponent_action, result):
    if result == Result.DRAW:
        return opponent_action

    if result == Result.WIN:
        return WEAKNESSES[opponent_action]
    return STRENGTHS[opponent_action]


if __name__ == '__main__':
    main()
