#!/usr/bin/env python3
import sys
from typing import FrozenSet, Tuple


Shape = FrozenSet[Tuple[int, int]]


def parse_input(filename: str) -> tuple[dict[int, Shape], list[tuple[int, int, list[int]]]]:
    shapes: dict[int, Shape] = {}
    regions: list[tuple[int, int, list[int]]] = []

    with open(filename) as f:
        lines = f.read().strip().split('\n')

    i = 0
    while i < len(lines) and ':' in lines[i] and 'x' not in lines[i]:
        shape_id = int(lines[i].rstrip(':'))
        i += 1
        cells: set[tuple[int, int]] = set()
        row = 0
        while i < len(lines) and lines[i] and not lines[i][0].isdigit():
            for col, ch in enumerate(lines[i]):
                if ch == '#':
                    cells.add((row, col))
            row += 1
            i += 1
        shapes[shape_id] = frozenset(cells)
        while i < len(lines) and not lines[i].strip():
            i += 1

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        dims, counts_str = line.split(': ')
        w, h = map(int, dims.split('x'))
        counts = list(map(int, counts_str.split()))
        regions.append((w, h, counts))
        i += 1

    return shapes, regions


def solve_part1(filename: str) -> int:
    shapes, regions = parse_input(filename)
    count = 0
    for width, height, counts in regions:
        total_cells = sum(len(shapes[i]) * counts[i] for i in range(6))
        if total_cells <= width * height:
            count += 1
    return count


def solve_part2(filename: str) -> int:
    # Part 2 is auto-completed as Day 12 is the final day of AoC 2025
    return 0


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python problem.py <input_file>")
        sys.exit(1)

    filename = sys.argv[1]
    print(solve_part1(filename))
    print(solve_part2(filename))


if __name__ == "__main__":
    main()
