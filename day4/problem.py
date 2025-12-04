#!/usr/bin/env python3
import sys
from pathlib import Path


def count_adjacent_rolls(grid: list[str], row: int, col: int) -> int:
    """Count paper rolls (@) in the 8 adjacent positions."""
    count = 0
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                count += 1
    return count


def solve_part1(grid: list[str]) -> int:
    """Count rolls that can be accessed by forklift (fewer than 4 adjacent rolls)."""
    count = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@':
                adjacent = count_adjacent_rolls(grid, row, col)
                if adjacent < 4:
                    count += 1
    return count


def count_adjacent_rolls_mutable(grid: list[list[str]], row: int, col: int) -> int:
    """Count paper rolls (@) in the 8 adjacent positions for mutable grid."""
    count = 0
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                count += 1
    return count


def solve_part2(grid: list[str]) -> int:
    """Count total rolls that can be removed by repeatedly accessing and removing."""
    mutable_grid = [list(row) for row in grid]
    total_removed = 0

    while True:
        to_remove: list[tuple[int, int]] = []
        for row in range(len(mutable_grid)):
            for col in range(len(mutable_grid[row])):
                if mutable_grid[row][col] == '@':
                    adjacent = count_adjacent_rolls_mutable(mutable_grid, row, col)
                    if adjacent < 4:
                        to_remove.append((row, col))

        if not to_remove:
            break

        for row, col in to_remove:
            mutable_grid[row][col] = '.'

        total_removed += len(to_remove)

    return total_removed


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python problem.py <input_file>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    lines = input_path.read_text().strip().split('\n')

    print(solve_part1(lines))
    print(solve_part2(lines))


if __name__ == "__main__":
    main()
