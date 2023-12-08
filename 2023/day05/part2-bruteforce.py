"""
Ugly bruteforce solution. But the code is simple and correct. Took ~6hours
"""
import dataclasses
import itertools
import time
from pathlib import Path

FILE_NAME = Path("input.txt")


@dataclasses.dataclass
class Mapping:
    destination_start: int
    source_start: int
    range: int

    def is_applicable(self, value: int) -> bool:
        return self.source_start <= value < (self.source_start + self.range)

    def map(self, value: int) -> int:
        return value + (self.destination_start - self.source_start)


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
        seed_blocks, mapping_groups = parse_file(f)

    lowest_location = None
    for seed_block_start, seed_block_range in seed_blocks:
        print("processing", (seed_block_start, seed_block_range))
        for seed in range(seed_block_start, seed_block_start + seed_block_range):
            mapped_value = seed
            for mapping_group in mapping_groups:
                mapped_value = mapping_group.map(mapped_value)

            if lowest_location is None or mapped_value < lowest_location:  # type: ignore[unreachable]
                lowest_location = mapped_value
        print(lowest_location)
    print(f"THE ANSWER IS: {lowest_location}")


def parse_file(f) -> tuple[list[tuple[int, int]], list[MappingGroup]]:
    seed_part, *mapping_parts = f.read().split("\n\n")
    seed_blocks = []
    seed_spec_numbers = [int(val) for val in seed_part.replace("seeds: ", "").split()]
    for seed_start, seed_range in itertools.batched(seed_spec_numbers, 2):
        seed_blocks.append((seed_start, seed_range))

    mapping_groups = []
    for mapping_block in mapping_parts:
        # first line can be dropped as it's just text
        mappings = []
        for line in mapping_block.strip().split("\n")[1:]:
            vals = [int(val) for val in line.split()]
            mappings.append(
                Mapping(destination_start=vals[0], source_start=vals[1], range=vals[2])
            )
        mapping_groups.append(MappingGroup(mappings=mappings))
    return sorted(seed_blocks, key=lambda block: block[0]), mapping_groups


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print("elapsed", time.monotonic() - start)
