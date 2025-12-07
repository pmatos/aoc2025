#!/usr/bin/env python3
import sys
from typing import TextIO
from collections import deque


def parse_input(f: TextIO) -> list[list[str]]:
    return [list(line.rstrip('\n')) for line in f]


def find_start(grid: list[list[str]]) -> tuple[int, int]:
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                return row, col
    return -1, -1


def part1(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    height = len(grid)
    width = len(grid[0]) if grid else 0

    start_row, start_col = find_start(grid)
    if start_row == -1:
        return 0

    splits = 0
    beams: deque[tuple[int, int]] = deque()
    beams.append((start_row, start_col))

    visited_splitters: set[tuple[int, int]] = set()

    while beams:
        row, col = beams.popleft()

        while True:
            row += 1

            if row < 0 or row >= height or col < 0 or col >= width:
                break

            cell = grid[row][col]

            if cell == '^':
                if (row, col) not in visited_splitters:
                    visited_splitters.add((row, col))
                    splits += 1
                    beams.append((row, col - 1))
                    beams.append((row, col + 1))
                break

    return splits


def part2(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    height = len(grid)
    width = len(grid[0]) if grid else 0

    start_row, start_col = find_start(grid)
    if start_row == -1:
        return 0

    col_counts: dict[int, int] = {start_col: 1}

    for row in range(start_row + 1, height):
        new_counts: dict[int, int] = {}
        for col, count in col_counts.items():
            if col < 0 or col >= width:
                continue
            cell = grid[row][col]
            if cell == '^':
                new_counts[col - 1] = new_counts.get(col - 1, 0) + count
                new_counts[col + 1] = new_counts.get(col + 1, 0) + count
            else:
                new_counts[col] = new_counts.get(col, 0) + count
        col_counts = new_counts

    return sum(col_counts.values())


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_file>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        grid = parse_input(f)

    result1 = part1(grid)
    print(result1)

    result2 = part2(grid)
    print(result2)


if __name__ == "__main__":
    main()
