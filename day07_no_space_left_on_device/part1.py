from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Directory:
    name: str
    parent_directory: Optional["Directory"]

    files: set["File"] = field(default_factory=set)
    directories: dict[str, "Directory"] = field(default_factory=dict)

    def get_absolute_path(self, suffix_path: Path = Path("")):
        if self.parent_directory is None:
            return Path("/") / suffix_path

        extended_suffix = Path(self.name) / suffix_path
        return self.parent_directory.get_absolute_path(extended_suffix)


@dataclass(frozen=True)
class File:
    name: str
    size: int


DIRECTORIES = []


def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f):
    total = 0
    for line in f.readlines():
        line = line.strip()

        is_command = line.startswith("$")
    return total


if __name__ == '__main__':
    main()
