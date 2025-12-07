#!/usr/bin/env python3
import sys
from typing import TextIO


def parse_input(f: TextIO) -> tuple[list[tuple[int, int]], list[int]]:
    ranges: list[tuple[int, int]] = []
    ingredients: list[int] = []

    parsing_ranges = True
    for line in f:
        line = line.strip()
        if not line:
            parsing_ranges = False
            continue

        if parsing_ranges:
            start, end = line.split("-")
            ranges.append((int(start), int(end)))
        else:
            ingredients.append(int(line))

    return ranges, ingredients


def is_fresh(ingredient_id: int, ranges: list[tuple[int, int]]) -> bool:
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def part1(ranges: list[tuple[int, int]], ingredients: list[int]) -> int:
    count = 0
    for ingredient in ingredients:
        if is_fresh(ingredient, ranges):
            count += 1
    return count


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []

    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged: list[tuple[int, int]] = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def part2(ranges: list[tuple[int, int]]) -> int:
    merged = merge_ranges(ranges)
    total = 0
    for start, end in merged:
        total += end - start + 1
    return total


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_file>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        ranges, ingredients = parse_input(f)

    result1 = part1(ranges, ingredients)
    print(result1)

    result2 = part2(ranges)
    print(result2)


if __name__ == "__main__":
    main()
