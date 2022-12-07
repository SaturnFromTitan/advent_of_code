from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Optional


@dataclass
class Directory:
    name: str
    parent_directory: Optional["Directory"]

    files: set["File"] = field(default_factory=set)
    directories: dict[str, "Directory"] = field(default_factory=dict)

    @lru_cache
    def get_absolute_path(self, suffix_path: Path = Path("")):
        if self.parent_directory is None:
            return Path("/") / suffix_path

        extended_suffix = Path(self.name) / suffix_path
        return self.parent_directory.get_absolute_path(extended_suffix)


@dataclass(frozen=True)
class File:
    name: str
    size: int


def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f):
    root = build_file_system(f)
    build_size_mapping(root)
    return "NOT READY"


def build_file_system(f):
    root = Directory(name="/", parent_directory=None)

    current_directory = root
    for line in f.readlines():
        line = line.strip()

        if line == "$ cd /":
            current_directory = root
            continue

        if line == "$ ls":
            continue

        if line == "$ cd ..":
            current_directory = current_directory.parent_directory
            continue

        cd_command = "$ cd "
        if line.startswith(cd_command):
            target_dir = line.replace(cd_command, "")
            current_directory = current_directory.directories[target_dir]
            continue

        part1, part2 = line.split(" ")
        if part1 == "dir":
            # entry is a (sub) directory
            name = part2
            sub_dir = Directory(name=name, parent_directory=current_directory)
            current_directory.directories[name] = sub_dir
        else:
            size, name = part1, part2
            # entry is a file
            try:
                size = int(size)
            except ValueError:
                print(f"Couldn't parse this line: {line}")
                raise

            file_ = File(name=name, size=size)
            current_directory.files.add(file_)
    return root


def build_size_mapping(root):
    ...


if __name__ == '__main__':
    main()
