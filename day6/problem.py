#!/usr/bin/env python3
import sys
from typing import TextIO


def parse_input(f: TextIO) -> list[list[str]]:
    lines = [line.rstrip('\n') for line in f]
    max_len = max(len(line) for line in lines) if lines else 0
    return [list(line.ljust(max_len)) for line in lines]


def is_blank_col(grid: list[list[str]], col: int) -> bool:
    return all(grid[row][col] == ' ' for row in range(len(grid)))


def find_problems(grid: list[list[str]], vertical: bool = False) -> list[tuple[list[int], str]]:
    if not grid:
        return []

    height = len(grid)
    width = len(grid[0])
    op_row = height - 1

    problems: list[tuple[list[int], str]] = []

    start_col = None
    for col in range(width + 1):
        if col == width or is_blank_col(grid, col):
            if start_col is not None:
                end_col = col - 1
                op = ''
                for c in range(start_col, end_col + 1):
                    if grid[op_row][c] in '+*':
                        op = grid[op_row][c]
                        break

                numbers: list[int] = []
                if vertical:
                    for c in range(start_col, end_col + 1):
                        digits = ''
                        for row in range(height - 1):
                            if grid[row][c].isdigit():
                                digits += grid[row][c]
                        if digits:
                            numbers.append(int(digits))
                else:
                    for row in range(height - 1):
                        segment = ''.join(grid[row][start_col:end_col + 1]).strip()
                        if segment and segment.isdigit():
                            numbers.append(int(segment))

                if numbers and op:
                    problems.append((numbers, op))
                start_col = None
        else:
            if start_col is None:
                start_col = col

    return problems


def solve_problem(numbers: list[int], op: str) -> int:
    if op == '+':
        return sum(numbers)
    else:
        result = 1
        for n in numbers:
            result *= n
        return result


def part1(grid: list[list[str]]) -> int:
    problems = find_problems(grid, vertical=False)
    total = 0
    for numbers, op in problems:
        total += solve_problem(numbers, op)
    return total


def part2(grid: list[list[str]]) -> int:
    problems = find_problems(grid, vertical=True)
    total = 0
    for numbers, op in problems:
        total += solve_problem(numbers, op)
    return total


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
