import operator
from typing import Optional

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}
INVERSE_OPERATORS = {
    "+": operator.sub,
    "-": operator.add,
    "*": operator.truediv,
    "/": operator.mul,
}
INPUT_FILE = "input.txt"


def main():
    with open(INPUT_FILE) as f:
        raw_jobs = parse_file(f)

    answer = solve_riddle(raw_jobs)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> dict[str, str]:
    raw_jobs = dict()
    for line in f.readlines():
        monkey_id, raw_job = line.strip().split(": ")
        raw_jobs[monkey_id] = raw_job
    return raw_jobs


def solve_riddle(raw_jobs):
    return find_humn_value(raw_jobs, "root", result_needed=None)


def find_humn_value(raw_jobs: dict[str, str], monkey_id: str, result_needed: Optional[int]) -> int:
    if monkey_id != "root":
        assert result_needed is not None

    if monkey_id == "humn":
        return result_needed

    raw_job = raw_jobs[monkey_id]
    monkey1_id, operator_raw, monkey2_id = raw_job.split()

    res1 = get_result(raw_jobs, monkey1_id)
    res2 = get_result(raw_jobs, monkey2_id)
    failed_monkey_id = monkey1_id if res1 is None else monkey2_id

    if monkey_id == "root":
        result_needed = res1 if res1 is not None else res2
    else:
        result_needed = get_new_result_needed(res1, res2, result_needed, operator_raw)
    return find_humn_value(raw_jobs, failed_monkey_id, result_needed)


def get_result(raw_jobs: dict[str, str], monkey_id: str) -> Optional[int]:
    try:
        return _get_result(raw_jobs, monkey_id)
    except ValueError:
        return None


def _get_result(raw_jobs: dict[str, str], monkey_id: str) -> int:
    if monkey_id == "humn":
        raise ValueError("That's the question...")

    raw_job = raw_jobs[monkey_id]
    if raw_job.isnumeric():
        return int(raw_job)

    monkey1_id, operation_raw, monkey2_id = raw_job.split()
    operation = OPERATORS[operation_raw]

    value1 = _get_result(raw_jobs, monkey1_id)
    value2 = _get_result(raw_jobs, monkey2_id)
    return operation(value1, value2)


def get_new_result_needed(val1, val2, result_needed, operator_raw):
    op = OPERATORS[operator_raw]
    inverse_op = INVERSE_OPERATORS[operator_raw]

    commutative_operators = {"+", "*"}
    if operator_raw in commutative_operators:
        # e.g.
        #     result_needed == val1 + val2
        # <=> result_needed - val2 == val1
        value = val1 if val1 is not None else val2
        return inverse_op(result_needed, value)

    if val1 is None:
        # e.g.
        #     result_needed == val1 / val2
        # <=> result_needed * val2 == val1
        return inverse_op(result_needed, val2)
    else:
        # e.g.
        #     result_needed == val1 / val2
        # <=> val2 = val1 / result_needed
        return op(val1, result_needed)


if __name__ == "__main__":
    main()
