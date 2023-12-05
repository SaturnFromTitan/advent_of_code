import dataclasses
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
        seeds, mapping_groups = parse_file(f)

    mapped_values = seeds.copy()
    for mapping_group in mapping_groups:
        mapped_values = [mapping_group.map(val) for val in mapped_values]
    lowest_location = min(mapped_values)
    print(f"THE ANSWER IS: {lowest_location}")


def parse_file(f) -> tuple[list[int], list[MappingGroup]]:
    seed_block, *mapping_blocks = f.read().split("\n\n")
    seeds = [int(val) for val in seed_block.replace("seeds: ", "").split()]

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


if __name__ == "__main__":
    main()
