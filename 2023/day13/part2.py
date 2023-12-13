import itertools


def main(file_name: str) -> None:
    with open(file_name) as f:
        patterns = parse_file(f)
    answer = sum([score(pattern) for pattern in patterns])
    print(f"THE ANSWER IS: {answer}")


def parse_file(f) -> list[str]:
    return f.read().strip().split("\n\n")


def score(pattern: str) -> int:
    rows = pattern.split("\n")
    double_rows = check_rows(rows)
    if double_rows:
        return 100 * double_rows

    double_columns = check_columns(rows)
    if double_columns:
        return double_columns
    raise ValueError(f"Didn't find a reflexion for this pattern\n{pattern}")


def check_columns(rows: list[str]) -> int:
    columns = ["".join([row[i] for row in rows]) for i in range(len(rows[0]))]
    return check_rows(columns)


def check_rows(lines: list[str]) -> int:
    reflection_candidates = _get_reflexion_candidates(lines)

    for idx, used_variant_for_candidate, _ in reflection_candidates:
        used_variant = used_variant_for_candidate
        length = min(len(lines) - 1 - idx, idx + 1)

        is_reflexion = True
        for offset in range(1, length):
            row1 = lines[idx - offset]
            row2 = lines[idx + 1 + offset]
            matches, used_variant_for_offset, _ = compare(
                row1, row2, allow_variants=not used_variant
            )
            used_variant = used_variant or used_variant_for_offset
            if not matches:
                is_reflexion = False

        if is_reflexion and used_variant:
            return idx + 1
    return 0


def _get_reflexion_candidates(lines: list[str]) -> list[tuple[int, bool, str]]:
    reflection_candidates = []
    for index, (row1, row2) in enumerate(itertools.pairwise(lines)):
        matches, with_variant, row1_variant = compare(row1, row2, allow_variants=True)
        if matches:
            reflection_candidates.append((index, with_variant, row1_variant))
    return reflection_candidates


def compare(line1: str, line2: str, allow_variants: bool) -> tuple[bool, bool, str]:
    if line1 == line2:
        return True, False, line1

    if allow_variants:
        for char_index, char in enumerate(line1):
            new_char = "." if char == "#" else "#"
            clean_line1 = line1[:char_index] + new_char + line1[char_index + 1 :]
            if clean_line1 == line2:
                return True, True, clean_line1
    return False, False, line1


if __name__ == "__main__":
    # must be higher than 38_726
    main("input.txt")
