import copy
import enum
import re
from dataclasses import dataclass, field

INPUT_FILE = "input.txt"


@dataclass
class Price:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0


@dataclass
class BluePrint:
    id: int
    price_ore_robot: Price
    price_clay_robot: Price
    price_obsidian_robot: Price
    price_geode_robot: Price


@dataclass
class Wallet:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def harvest(self, garage):
        self.ore += garage.ore_robots
        self.clay += garage.clay_robots
        self.obsidian += garage.obsidian_robots
        self.geode += garage.geode_robots

    def pay(self, price):
        self.ore -= price.ore
        self.clay -= price.clay
        self.obsidian -= price.obsidian


@enum.unique
class Action(enum.Enum):
    BUILD_NOTHING = "build_nothing"
    BUILD_ORE_ROBOT = "build_ore_robot"
    BUILD_CLAY_ROBOT = "build_clay_robot"
    BUILD_OBSIDIAN_ROBOT = "build_obsidian_robot"
    BUILD_GEODE_ROBOT = "build_geode_robot"


@dataclass
class Garage:
    ore_robots: int = 1
    clay_robots: int = 0
    obsidian_robots: int = 0
    geode_robots: int = 0

    def add_robot(self, action):
        if action == Action.BUILD_ORE_ROBOT:
            self.ore_robots += 1
        elif action == Action.BUILD_CLAY_ROBOT:
            self.clay_robots += 1
        elif action == Action.BUILD_OBSIDIAN_ROBOT:
            self.obsidian_robots += 1
        elif action == Action.BUILD_GEODE_ROBOT:
            self.geode_robots += 1


@dataclass
class State:
    blueprint: BluePrint
    minutes_passed: int = 0
    wallet: Wallet = field(default_factory=Wallet)
    garage: Garage = field(default_factory=Garage)

    max_minutes: int = field(default=24, init=False)

    def minutes_remaining(self):
        return self.max_minutes - self.minutes_passed

    def time_is_up(self):
        return self.minutes_passed >= self.max_minutes

    def get_actions(self):
        blueprint = self.blueprint
        prices = [
            blueprint.price_geode_robot,
            blueprint.price_obsidian_robot,
            blueprint.price_clay_robot,
            blueprint.price_ore_robot,
        ]
        max_ore_price = max([price.ore for price in prices])

        if self.can_pay(price := blueprint.price_geode_robot):
            # If you can buy a geode robot, you should do so
            return [(Action.BUILD_GEODE_ROBOT, price)]

        if self.minutes_passed == self.max_minutes - 1:
            # if there's just one minute left, then only building
            # geode robots makes a difference
            return [(Action.BUILD_NOTHING, Price())]

        if self.can_pay(price := blueprint.price_obsidian_robot):
            # If you can buy a geode robot, you should do so
            return [(Action.BUILD_OBSIDIAN_ROBOT, price)]

        actions = [(Action.BUILD_NOTHING, Price())]

        ore_robot_price = blueprint.price_ore_robot
        if (
            # since we can only buy one robot at a time, there's no point
            # in producing more ore than any robot requires
            self.garage.ore_robots < max_ore_price and self.can_pay(ore_robot_price)
        ):
            actions.append((Action.BUILD_ORE_ROBOT, ore_robot_price))

        if self.can_pay(price := blueprint.price_clay_robot):
            actions.append((Action.BUILD_CLAY_ROBOT, price))
        return actions

    def can_pay(self, price):
        return (
            self.wallet.ore >= price.ore
            and self.wallet.clay >= price.clay
            and self.wallet.obsidian >= price.obsidian
        )


def main():
    with open(INPUT_FILE) as f:
        blueprints = parse_file(f)

    answer = get_quality_levels(blueprints)
    print(f"THE ANSWER IS: {answer}")


def parse_file(f):
    blueprints = list()
    for line in f.readlines():
        line = line.strip()

        pattern = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
        groups = re.match(pattern, line).groups()
        (
            blueprint_id,
            ore_robot_price_ore,
            clay_robot_price_ore,
            obsidian_robot_price_ore,
            obsidian_robot_price_clay,
            geode_robot_price_ore,
            geode_robot_price_obsidian,
        ) = map(int, groups)
        blueprint = BluePrint(
            id=blueprint_id,
            price_ore_robot=Price(ore=ore_robot_price_ore),
            price_clay_robot=Price(ore=clay_robot_price_ore),
            price_obsidian_robot=Price(
                ore=obsidian_robot_price_ore, clay=obsidian_robot_price_clay
            ),
            price_geode_robot=Price(
                ore=geode_robot_price_ore, obsidian=geode_robot_price_obsidian
            ),
        )
        blueprints.append(blueprint)
    return blueprints


def get_quality_levels(blueprints):
    answer = 0
    for blueprint in blueprints:
        print("BLUEPRINT:", blueprint.id)
        num_geode = get_max_geode_score(blueprint)
        quality_level = blueprint.id * num_geode
        print("\tquality_level:", quality_level)
        answer += quality_level
    return answer


def get_max_geode_score(blueprint):
    max_geode = 0
    start = State(blueprint=blueprint)

    queue = [start]
    while queue:
        state = queue.pop()

        for action, price in state.get_actions():
            new_wallet = copy.deepcopy(state.wallet)
            new_wallet.harvest(state.garage)
            new_wallet.pay(price)

            new_garage = copy.deepcopy(state.garage)
            new_garage.add_robot(action)

            new_state = State(
                blueprint=state.blueprint,
                minutes_passed=state.minutes_passed + 1,
                wallet=new_wallet,
                garage=new_garage,
            )
            if new_state.time_is_up():
                max_geode = max(max_geode, new_state.wallet.geode)
                continue

            upper_bound = get_upper_bound_geode_harvesting(new_state)
            if upper_bound < max_geode:
                continue

            queue.append(new_state)
    return max_geode


def get_upper_bound_geode_harvesting(state):
    """
    How much geode could still be harvested, assuming we get a new geode robot
    every minute for all the remaining time
    """
    upper_bound = state.wallet.geode
    geode_production = state.garage.geode_robots
    for _ in range(state.minutes_remaining()):
        upper_bound += geode_production
        geode_production += 1
    return upper_bound


if __name__ == "__main__":
    main()
