import math
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: Callable[[int], int]
    test_divisor: int
    if_true_monkey: int
    if_false_monkey: int

    def get_next_monkey_id(self, item):
        if self._test(item):
            return self.if_true_monkey
        return self.if_false_monkey

    def _test(self, item):
        return item % self.test_divisor == 0


MONKEYS = [
    Monkey(
        id=0,
        items=[56, 56, 92, 65, 71, 61, 79],
        operation=lambda old: old * 7,
        test_divisor=3,
        if_true_monkey=3,
        if_false_monkey=7,
    ),
    Monkey(
        id=1,
        items=[61, 85],
        operation=lambda old: old + 5,
        test_divisor=11,
        if_true_monkey=6,
        if_false_monkey=4,
    ),
    Monkey(
        id=2,
        items=[54, 96, 82, 78, 69],
        operation=lambda old: old * old,
        test_divisor=7,
        if_true_monkey=0,
        if_false_monkey=7,
    ),
    Monkey(
        id=3,
        items=[57, 59, 65, 95],
        operation=lambda old: old + 4,
        test_divisor=2,
        if_true_monkey=5,
        if_false_monkey=1,
    ),
    Monkey(
        id=4,
        items=[62, 67, 80],
        operation=lambda old: old * 17,
        test_divisor=19,
        if_true_monkey=2,
        if_false_monkey=6,
    ),
    Monkey(
        id=5,
        items=[91],
        operation=lambda old: old + 7,
        test_divisor=5,
        if_true_monkey=1,
        if_false_monkey=4,
    ),
    Monkey(
        id=6,
        items=[79, 83, 64, 52, 77, 56, 63, 92],
        operation=lambda old: old + 6,
        test_divisor=17,
        if_true_monkey=2,
        if_false_monkey=0,
    ),
    Monkey(
        id=7,
        items=[50, 97, 76, 96, 80, 56],
        operation=lambda old: old + 3,
        test_divisor=13,
        if_true_monkey=3,
        if_false_monkey=5,
    ),
]
MONKEYS_BY_ID = {m.id: m for m in MONKEYS}


def main():
    inspection_counter = {m.id: 0 for m in MONKEYS}

    # need a divisor that doesn't influence the remainders in all monkey's test's
    # -> use modulo of item value with the least common multiple of all monkey divisor
    # (since all monkey divisors are prime, that's just the multiple of all divisors)
    factor = math.lcm(*[monkey.test_divisor for monkey in MONKEYS])

    for i in range(10000):
        for monkey in MONKEYS:
            for item in monkey.items:
                inspection_counter[monkey.id] += 1

                inspected_item = monkey.operation(item)
                inspected_item = inspected_item % factor

                next_monkey_id = monkey.get_next_monkey_id(inspected_item)
                next_monkey = MONKEYS_BY_ID[next_monkey_id]

                next_monkey.items.append(inspected_item)

            # assumes that monkeys can't pass items to themselves
            del monkey.items[:]

    sorted_monkey_activity = sorted(
        inspection_counter.items(), key=lambda x: x[1], reverse=True
    )
    most_active_monkeys = sorted_monkey_activity[:2]
    answer = most_active_monkeys[0][1] * most_active_monkeys[1][1]
    print(f"THE ANSWER: {answer}")


if __name__ == "__main__":
    main()
