import dataclasses
import itertools
from pathlib import Path

FILE_NAME = Path("input.txt")

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
    print_seed_blocks(seed_blocks)
    for i, mapping_group in enumerate(mapping_groups):
        seed_blocks = _map_seed_blocks(seed_blocks, mapping_group)
        seed_blocks = merge(seed_blocks)
        print()
        print_seed_blocks(seed_blocks)
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

    sorted_mappings = sorted(mapping_group.mappings, key=lambda m: m.source_start)
    lowest_source_start = min(m.source_start for m in sorted_mappings)
    highest_source_end = max(m.source_end for m in sorted_mappings)

    result_blocks = []

    if seed_start < lowest_source_start:
        result_blocks.append((seed_start, min(seed_end, lowest_source_start - 1)))

    last_source_end = None
    for mapping in sorted_mappings:
        if seed_start > mapping.source_end:
            continue

        # check for "holes" in the mapping group
        if last_source_end is not None and last_source_end + 1 < mapping.source_start:
            result_blocks.append(
                (
                    max(seed_start, last_source_end + 1),
                    min(seed_end, mapping.source_start - 1),
                )
            )

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

    print(result_blocks)
    print(merge(result_blocks))
    return merge(result_blocks)
    # return result_blocks


def print_seed_blocks(blocks: list[SeedBlock]) -> None:
    sorted_blocks = sorted(blocks, key=lambda b: b[0])
    print([(f"{block[0]:_}", f"{block[1]:_}") for block in sorted_blocks])


def merge(blocks: list[SeedBlock]) -> list[SeedBlock]:
    if not blocks:
        return []

    new_blocks = []

    sorted_blocks = sorted(blocks, key=lambda b: b[0])
    print(sorted_blocks)

    last_end = None
    merged_block_start = None
    for block in sorted_blocks:
        print(block, merged_block_start, last_end)
        if last_end is None:
            last_end = block[1]
            if merged_block_start is None:
                merged_block_start = block[0]
            continue

        if last_end + 1 < block[0]:
            new_blocks.append((merged_block_start, last_end))
            last_end = block[1]
            merged_block_start = block[0]
        else:
            last_end = block[1]

    if merged_block_start:
        new_blocks.append((merged_block_start, sorted_blocks[-1][1]))
    else:
        new_blocks.append(block)
    return new_blocks


if __name__ == "__main__":
    assert merge([(10, 49), (60, 69), (60, 90)]) == [(10, 49), (60, 90)]
    assert merge([(0, 4), (15, 24), (10, 19), (35, 89), (92, 92)]) == [
        (0, 4),
        (10, 24),
        (35, 89),
        (92, 92),
    ]

    # test case 1: seed block > mappings
    seed_block = (10, 90)
    mapping_group = MappingGroup(
        mappings=[
            Mapping(destination_start=-100, source_start=0, range=10),
        ]
    )
    expected = [(10, 90)]
    assert _map_seed_block(seed_block, mapping_group) == expected
    print("test case 1 passed")

    # test case 2: seed block < mappings
    seed_block = (10, 90)
    mapping_group = MappingGroup(
        mappings=[
            Mapping(destination_start=-100, source_start=91, range=10),
        ]
    )
    expected = [(10, 90)]
    assert _map_seed_block(seed_block, mapping_group) == expected
    print("test case 2 passed")

    # test case 3: mapping group with holes, starting & ending 'outside' of seed block
    seed_block = (10, 90)
    mapping_group = MappingGroup(
        mappings=[
            Mapping(destination_start=-5, source_start=5, range=10),
            Mapping(destination_start=10, source_start=25, range=10),
            Mapping(destination_start=92, source_start=90, range=5),
        ]
    )
    # expected = [(0, 4), (15, 24), (10, 19), (35, 89), (92, 92)]
    expected = [(0, 4), (10, 24), (35, 89), (92, 92)]
    res = _map_seed_block(seed_block, mapping_group)
    assert res == expected, res
    print("test case 3 passed")

    # test case 4: mapping group with holes, starting & ending 'inside' of seed block
    seed_block = (10, 90)
    mapping_group = MappingGroup(
        mappings=[
            Mapping(destination_start=-5, source_start=15, range=1),
            Mapping(destination_start=10, source_start=25, range=10),
        ]
    )
    # expected = [(10, 14), (-5, -5), (16, 24), (10, 19), (35, 90)]
    expected = [(-5, -5), (10, 24), (35, 90)]
    res = _map_seed_block(seed_block, mapping_group)
    assert res == expected, res
    print("test case 4 passed")

    # test case 5: 1 mapping just inside the seed block
    seed_block = (10, 90)
    mapping_group = MappingGroup(
        mappings=[
            Mapping(destination_start=60, source_start=50, range=10),
        ]
    )
    expected = [(10, 49), (60, 90)]
    assert _map_seed_block(seed_block, mapping_group) == expected
    print("test case 5 passed")

    print()
    print("*" * 50)
    print()

    assert merge([(10, 49), (60, 69), (60, 90)]) == [(10, 49), (60, 90)]

    # run
    main()
