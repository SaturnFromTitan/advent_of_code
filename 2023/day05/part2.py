import dataclasses
import itertools
from pathlib import Path

FILE_NAME = Path("example_input.txt")

SeedBlock = tuple[int, int]


@dataclasses.dataclass
class Mapping:
    destination_start: int
    source_start: int
    range: int

    @property
    def source_end(self):
        return self.source_start + self.range - 1

    @property
    def destination_end(self):
        return self.destination_start + self.range - 1

    def map(self, value: int) -> int:
        diff = self.destination_start - self.source_start
        return value + diff


@dataclasses.dataclass
class MappingGroup:
    mappings: list[Mapping]


def main() -> None:
    with open(FILE_NAME) as f:
        seed_blocks, mapping_groups = parse_file(f)

    result_blocks = map_seed_blocks(seed_blocks, mapping_groups)
    answer = min([block[0] for block in result_blocks])
    print(f"THE ANSWER IS: {answer:_}")


def parse_file(f) -> tuple[list[SeedBlock], list[MappingGroup]]:
    print("parsing file")
    seed_block, *mapping_blocks = f.read().split("\n\n")

    seed_blocks = []
    seed_spec_numbers = [int(val) for val in seed_block.replace("seeds: ", "").split()]
    for seed_start, seed_range in list(itertools.pairwise(seed_spec_numbers))[::2]:
        seed_blocks.append((seed_start, seed_start + seed_range - 1))

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
    return seed_blocks, mapping_groups


def map_seed_blocks(
    seed_blocks: list[SeedBlock], mapping_groups: list[MappingGroup]
) -> list[SeedBlock]:
    print("mapping seed blocks")
    # print_seed_blocks(seed_blocks)
    for i, mapping_group in enumerate(mapping_groups):
        seed_blocks = _map_seed_blocks(seed_blocks, mapping_group)
        # print_seed_blocks(seed_blocks)
    return seed_blocks


def _map_seed_blocks(
    seed_blocks: list[SeedBlock], mapping_group: MappingGroup
) -> list[SeedBlock]:
    result_blocks = []
    for seed_block in seed_blocks:
        result_blocks.extend(_map_seed_block(seed_block, mapping_group))
    return result_blocks


def _map_seed_block(
    seed_block: SeedBlock, mapping_group: MappingGroup
) -> list[SeedBlock]:
    seed_start, seed_end = seed_block

    lowest_source_start = min([m.source_start for m in mapping_group.mappings])
    highest_source_end = max([m.source_end for m in mapping_group.mappings])

    result_blocks = []

    if seed_start < lowest_source_start:
        result_blocks.append((seed_start, min(seed_end, lowest_source_start - 1)))

    last_source_end = lowest_source_start - 1
    for mapping in sorted(mapping_group.mappings, key=lambda m: m.source_start):
        if seed_start > mapping.source_end:
            last_source_end = mapping.source_end
            continue

        # check for "holes" in the mapping group
        if last_source_end + 1 != mapping.source_start:
            result_blocks.append((last_source_end + 1, mapping.source_start - 1))

        if seed_end < mapping.source_start:
            break

        result_blocks.append(
            (
                mapping.map(max(seed_start, mapping.source_start)),
                mapping.map(min(seed_end, mapping.source_end)),
            )
        )
        last_source_end = mapping.source_end

    if seed_end > highest_source_end:
        result_blocks.append((max(seed_start, highest_source_end + 1), seed_end))

    return result_blocks


def print_seed_blocks(blocks: list[SeedBlock]) -> None:
    print(sorted(blocks, key=lambda b: b[0]))


if __name__ == "__main__":
    main()
