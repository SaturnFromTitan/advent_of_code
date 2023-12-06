import dataclasses
import itertools
from pathlib import Path

FILE_NAME = Path("input.txt")


@dataclasses.dataclass
class Mapping:
    destination_start: int
    source_start: int
    range: int

    def is_applicable(self, value: int) -> bool:
        return self.source_start <= value < (self.source_start + self.range)

    @property
    def diff(self) -> int:
        return self.destination_start - self.source_start

    def map(self, value: int) -> int:
        return value + self.diff


@dataclasses.dataclass
class MappingGroup:
    mappings: list[Mapping]

    def map(self, value: int) -> int:
        for mapping in self.mappings:
            if mapping.is_applicable(value):
                return mapping.map(value)
        return value


def main() -> None:
    with open(FILE_NAME) as f:
        seeds, mapping_groups = parse_file(f)

    for mapping_group in mapping_groups:
        min_diff = min([mapping.diff for mapping in mapping_group.mappings])
        print(min_diff)
    raise SystemExit

    mapped_values = seeds.copy()
    for mapping_group in mapping_groups:
        mapped_values = [mapping_group.map(val) for val in mapped_values]
        print("mapping applied")

    print()
    print_nums(seeds)
    print_nums(mapped_values)
    diffs = [location - seed for (seed, location) in zip(seeds, mapped_values)]
    print_nums(diffs)
    lowest_location = min(mapped_values)
    print(f"THE ANSWER IS: {lowest_location:_}")


def parse_file(f) -> tuple[list[int], list[MappingGroup]]:
    print("parsing file")
    seed_block, *mapping_blocks = f.read().split("\n\n")

    # seeds = []
    # seed_spec_numbers = [int(val) for val in seed_block.replace("seeds: ", "").split()]
    # for seed_start, seed_range in list(itertools.pairwise(seed_spec_numbers))[::2]:
    #     seeds.extend([seed_start, seed_start + seed_range - 1])
    seed_start, seed_range = 1117825174, 279314434
    seeds = [seed_start] + [seed_start + 10**i for i in range(len(str(seed_range)) + 1)]

    mapping_groups = []
    for mapping_block in mapping_blocks:
        # first line can be dropped as it's just text
        mappings = []
        for line in mapping_block.strip().split("\n")[1:]:
            vals = [int(val) for val in line.split()]
            mappings.append(
                Mapping(destination_start=vals[0], source_start=vals[1], range=vals[2])
            )
        mapping_groups.append(MappingGroup(mappings=mappings))
    return seeds, mapping_groups


def print_nums(values: list[int]) -> None:
    parts = [
        f"({val1:_}, {val2:_})"
        for (val1, val2) in list(itertools.pairwise(values))[::2]
    ]
    output = "[" + ", ".join(parts) + "]"
    print(output)


if __name__ == "__main__":
    main()
