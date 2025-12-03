#!/usr/bin/env python3
import sys
from pathlib import Path


def max_joltage(bank: str) -> int:
    """Find maximum two-digit number from bank where first digit comes before second."""
    digits = [int(c) for c in bank]
    n = len(digits)

    max_right = [0] * n
    max_right[n - 1] = 0
    running_max = digits[n - 1]
    for i in range(n - 2, -1, -1):
        max_right[i] = running_max
        running_max = max(running_max, digits[i])

    maximum = 0
    for i in range(n - 1):
        value = digits[i] * 10 + max_right[i]
        maximum = max(maximum, value)

    return maximum


def solve_part1(lines: list[str]) -> int:
    """Sum of maximum joltage from each bank."""
    total = 0
    for line in lines:
        if line.strip():
            total += max_joltage(line.strip())
    return total


def max_joltage_k(bank: str, k: int) -> int:
    """Find maximum k-digit number by selecting k digits in order."""
    digits = [int(c) for c in bank]
    n = len(digits)

    result = []
    pos = 0
    for remaining in range(k, 0, -1):
        end = n - remaining + 1
        max_digit = -1
        max_pos = -1
        for i in range(pos, end):
            if digits[i] > max_digit:
                max_digit = digits[i]
                max_pos = i
        result.append(max_digit)
        pos = max_pos + 1

    return int(''.join(str(d) for d in result))


def solve_part2(lines: list[str]) -> int:
    """Sum of maximum 12-digit joltage from each bank."""
    total = 0
    for line in lines:
        if line.strip():
            total += max_joltage_k(line.strip(), 12)
    return total


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
