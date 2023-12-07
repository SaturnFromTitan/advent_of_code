import dataclasses
import itertools
import typing
from pathlib import Path

FILE_NAME = Path("example_input.txt")

SeedBlock = tuple[int, int]
MapFunc = typing.Callable[[int], int]


@dataclasses.dataclass
class Mapping:
    start: int
    end: int
    diff: int

    @classmethod
    def from_spec(
        cls, destination_start: int, source_start: int, range_length: int
    ) -> "Mapping":
        return cls(
            start=source_start,
            end=source_start + range_length - 1,
            diff=destination_start - source_start,
        )

    def map(self, value: int) -> int:
        return value + self.diff


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
            mappings.append(Mapping.from_spec(*vals))
        mapping_groups.append(MappingGroup(mappings=mappings))
    return seed_blocks, mapping_groups


def map_seed_blocks(
    seed_blocks: list[SeedBlock], mapping_groups: list[MappingGroup]
) -> list[SeedBlock]:
    print("mapping seed blocks")
    print_seed_blocks(seed_blocks)
    for i, mapping_group in enumerate(mapping_groups):
        seed_blocks = _map_seed_blocks(seed_blocks, mapping_group)
        # seed_blocks = merge(seed_blocks)
        print()
        print_seed_blocks(seed_blocks)
        raise SystemExit
    return seed_blocks


def _map_seed_blocks(
    seed_blocks: list[SeedBlock], mapping_group: MappingGroup
) -> list[SeedBlock]:
    result_blocks = []
    for seed_block in seed_blocks:
        result_blocks.extend(_map_seed_block(seed_block, mapping_group))
    return result_blocks


# def _map_seed_block(
#     seed_block: SeedBlock, mapping_group: MappingGroup
# ) -> list[SeedBlock]:
#     result_blocks = []
#     for mapping in mapping_group.mappings:
#         result_blocks.extend(get_interval_blocks(seed_block, mapping))
#     # return merge(result_blocks)
#     return result_blocks


# def _map_seed_block(
#     seed_block: SeedBlock, mapping_group: MappingGroup
# ) -> list[SeedBlock]:
#     seed_start, seed_end = seed_block
#     markers = get_markers(seed_block, mapping_group)
#     res = [
#         (func(max(seed_start, marker_start)), func(min(seed_end, marker_end)))
#         for (marker_start, marker_end), func in get_markers(seed_block, mapping_group)
#         if (marker_start >= seed_start) or (marker_end <= seed_end)
#     ]
#     print(markers)
#     print(res)
#     raise SystemExit
#     return res
#
#
# def get_markers(
#     seed_block: SeedBlock, mapping_group: MappingGroup
# ) -> list[tuple[SeedBlock, MapFunc]]:
#     seed_start, seed_end = seed_block
#     sorted_mappings = sorted(mapping_group.mappings, key=lambda m: m.start)
#
#     last_mapping = None
#     markers: list[tuple[SeedBlock, MapFunc]] = []
#     for mapping in sorted_mappings:
#         if (mapping.end < seed_start) or (mapping.start > seed_end):
#             continue
#
#         markers.append(((mapping.start, mapping.end), mapping.map))
#         if last_mapping and last_mapping.end + 1 < mapping.start:
#             markers.append(
#                 ((last_mapping.end + 1, mapping.start - 1), lambda x: x)
#             )
#
#         last_mapping = mapping
#
#     lowest_source_start = min(m.start for m in sorted_mappings)
#     if seed_start < lowest_source_start:
#         markers.append(((seed_start, lowest_source_start - 1), lambda x: x))
#
#     highest_source_end = max(m.end for m in sorted_mappings)
#     if seed_end > highest_source_end:
#         markers.append(((highest_source_end + 1, seed_end), lambda x: x))
#
#     return markers


# def _map_seed_block(seed_block: SeedBlock, mapping_group: MappingGroup) -> list[SeedBlock]:
#     mg_start = min(m.start for m in mapping_group.mappings)
#     mg_end = max(m.end for m in mapping_group.mappings)
#
#     # seed block is completely left or completely right of mapping internal
#     # <--S-->
#     #          <--I-->
#     # OR
#     #          <--S-->
#     # <--I-->
#     seed_start, seed_end = seed_block
#     if (mg_end < seed_start) or (mg_start > seed_end):
#         return [seed_block]
#
#     # -> there's some overlap of interval mapping & seed block
#     sorted_mappings = [
#         mapping
#         for mapping in sorted(mapping_group.mappings, key=lambda m: m.start)
#         if (mapping.end >= seed_start) or (mapping.start <= seed_end)
#     ]
#
#
#
#     # seed block is contained within mapping internal (borders can be equal)
#     #      <--S-->
#     #    <----I---->
#     if mg_start <= seed_start and seed_end <= mg_end:
#         for mapping in sorted_mappings:
#
#         return [(mapping.map(seed_start), mapping.map(seed_end))]
#
#     # mapping interval is contained within seed block (borders can't be equal)
#     #    <----S---->
#     #      <--I-->
#     if seed_start < mg_start and mg_end < seed_end:
#         return [
#             (seed_start, mg_start - 1),
#             (mapping.map(mg_start), mapping.map(mg_end)),
#             (mg_end + 1, seed_end),
#         ]
#
#     # mapping interval overlaps on the left
#     #    <--S-->
#     #       <--I-->
#     if seed_start < mg_start and seed_end <= mg_end:
#         return [
#             (seed_start, mg_start - 1),
#             (mapping.map(mg_start), mapping.map(seed_end)),
#         ]
#
#     # mapping interval overlaps on the right
#     #       <--S-->
#     #    <--I-->
#     if mg_start <= seed_start and mg_end < seed_end:
#         return [
#             (mapping.map(seed_start), mapping.map(mg_end)),
#             (mg_end + 1, seed_end),
#         ]
#
#     print(seed_block, mapping)
#     raise ValueError("Well that's unexpected")


# def identity(value: int) -> int:
#     return value


def print_seed_blocks(blocks: list[SeedBlock]) -> None:
    sorted_blocks = sorted(blocks, key=lambda b: b[0])
    print([(f"{block[0]:_}", f"{block[1]:_}") for block in sorted_blocks])


def merge(blocks: list[SeedBlock]) -> list[SeedBlock]:
    if not blocks:
        return []

    new_blocks = []

    sorted_blocks = sorted(blocks, key=lambda b: b[0])

    last_end = None
    merged_block_start = None
    for block in sorted_blocks:
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
    # blocks = [(90, 98)]
    # mg = MappingGroup(mappings=[
    #     Mapping(destination_start=60, source_start=56, range=37),
    #     Mapping(destination_start=56, source_start=93, range=4),
    # ])
    # assert _map_seed_blocks(blocks, mg) == [(56, 59), (94, 98)]
    #
    # assert merge([(10, 49), (60, 69), (60, 90)]) == [(10, 49), (60, 90)]
    # assert merge([(0, 4), (15, 24), (10, 19), (35, 89), (92, 92)]) == [
    #     (0, 4),
    #     (10, 24),
    #     (35, 89),
    #     (92, 92),
    # ]
    #
    # # test case 1: seed block > mappings
    # seed_block = (10, 90)
    # mapping_group = MappingGroup(
    #     mappings=[
    #         Mapping(destination_start=-100, source_start=0, range=10),
    #     ]
    # )
    # expected = [(10, 90)]
    # res = _map_seed_block(seed_block, mapping_group)
    # assert res == expected, res
    # print("test case 1 passed")
    #
    # # test case 2: seed block < mappings
    # seed_block = (10, 90)
    # mapping_group = MappingGroup(
    #     mappings=[
    #         Mapping(destination_start=-100, source_start=91, range=10),
    #     ]
    # )
    # expected = [(10, 90)]
    # assert _map_seed_block(seed_block, mapping_group) == expected
    # print("test case 2 passed")
    #
    # # test case 3: mapping group with holes, starting & ending 'outside' of seed block
    # seed_block = (10, 90)
    # mapping_group = MappingGroup(
    #     mappings=[
    #         Mapping(destination_start=-5, source_start=5, range=10),
    #         Mapping(destination_start=10, source_start=25, range=10),
    #         Mapping(destination_start=92, source_start=90, range=5),
    #     ]
    # )
    # expected = [(0, 4), (10, 24), (35, 89), (92, 92)]
    # res = _map_seed_block(seed_block, mapping_group)
    # assert res == expected, res
    # print("test case 3 passed")
    #
    # # test case 4: mapping group with holes, starting & ending 'inside' of seed block
    # seed_block = (10, 90)
    # mapping_group = MappingGroup(
    #     mappings=[
    #         Mapping(destination_start=-5, source_start=15, range=1),
    #         Mapping(destination_start=10, source_start=25, range=10),
    #     ]
    # )
    # # expected = [(10, 14), (-5, -5), (16, 24), (10, 19), (35, 90)]
    # expected = [(-5, -5), (10, 24), (35, 90)]
    # res = _map_seed_block(seed_block, mapping_group)
    # assert res == expected, res
    # print("test case 4 passed")
    #
    # # test case 5: 1 mapping just inside the seed block
    # seed_block = (10, 90)
    # mapping_group = MappingGroup(
    #     mappings=[
    #         Mapping(destination_start=60, source_start=50, range=10),
    #     ]
    # )
    # expected = [(10, 49), (60, 90)]
    # assert _map_seed_block(seed_block, mapping_group) == expected
    # print("test case 5 passed")
    #
    # print()
    # print("*" * 50)
    # print()
    #
    # assert merge([(10, 49), (60, 69), (60, 90)]) == [(10, 49), (60, 90)]

    # run
    main()
