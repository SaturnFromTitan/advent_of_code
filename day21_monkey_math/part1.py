import operator

OPERATIONS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}
INPUT_FILE = "input.txt"


def main():
    with open(INPUT_FILE) as f:
        raw_jobs = parse_file(f)

    answer = get_result(raw_jobs, monkey_id="root")
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> dict[str, str]:
    raw_jobs = dict()
    for line in f.readlines():
        monkey_id, raw_job = line.strip().split(": ")
        raw_jobs[monkey_id] = raw_job
    return raw_jobs


def get_result(raw_jobs: dict[str, str], monkey_id: str) -> int:
    raw_job = raw_jobs[monkey_id]
    if raw_job.isnumeric():
        return int(raw_job)

    monkey1_id, operation_raw, monkey2_id = raw_job.split()
    operation = OPERATIONS[operation_raw]
    value1 = get_result(raw_jobs, monkey_id=monkey1_id)
    value2 = get_result(raw_jobs, monkey_id=monkey2_id)
    return operation(value1, value2)


if __name__ == '__main__':
    main()
