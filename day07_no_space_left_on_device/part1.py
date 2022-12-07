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

    _size: int = 0

    # @lru_cache
    # def get_absolute_path(self, suffix_path: Path = Path("")):
    #     if self.parent_directory is None:
    #         return Path("/") / suffix_path
    #
    #     extended_suffix = Path(self.name) / suffix_path
    #     return self.parent_directory.get_absolute_path(extended_suffix)

    def get_size(self):
        # !Caution!
        #   this method should only be used after the whole file system was parsed. The cached
        #   value doesn't change once it was computed.
        if self._size:
            return self._size

        size_of_files = sum([file.size for file in self.files])
        size_of_directories = sum([sub_dir.get_size() for sub_dir in self.directories.values()])
        self._size = size_of_files + size_of_directories
        return self._size


@dataclass(frozen=True)
class File:
    name: str
    size: int


DIRECTORIES = list()


def main():
    with open("input.txt") as f:
        answer = process_file(f)
    print(f"THE ANSWER IS: {answer}")


def process_file(f):
    build_file_system(f)
    return compute_answer()


def build_file_system(f):
    root = Directory(name="/", parent_directory=None)
    DIRECTORIES.append(root)

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
            DIRECTORIES.append(sub_dir)
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


def compute_answer():
    limit = 100_000
    dirs_and_sizes = [(dir_, dir_.get_size()) for dir_ in DIRECTORIES]
    small_dir_sizes = [size for (dir_, size) in dirs_and_sizes if size <= limit]
    return sum(small_dir_sizes)


if __name__ == '__main__':
    main()
