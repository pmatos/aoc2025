#!/usr/bin/env python3
import sys


def is_invalid_id(n: int) -> bool:
    """Check if a number is an invalid ID (digits repeated twice)."""
    s = str(n)
    if len(s) % 2 != 0:
        return False
    half = len(s) // 2
    return s[:half] == s[half:]


def generate_invalid_ids_in_range(start: int, end: int) -> list[int]:
    """Generate all invalid IDs in the given range [start, end]."""
    invalid_ids = []

    # For each possible half-length, generate invalid IDs
    # An invalid ID of length 2n is formed by X repeated twice where X has n digits
    # Invalid ID = X * 10^n + X = X * (10^n + 1)

    n = 1
    while True:
        multiplier = 10**n + 1
        min_x = 10**(n-1) if n > 1 else 1
        max_x = 10**n - 1

        # The smallest invalid ID with this n
        min_invalid = min_x * multiplier
        # The largest invalid ID with this n
        max_invalid = max_x * multiplier

        if min_invalid > end:
            break

        # Find the range of X values that produce invalid IDs in [start, end]
        # X * multiplier >= start  =>  X >= start / multiplier
        # X * multiplier <= end    =>  X <= end / multiplier

        x_start = max(min_x, (start + multiplier - 1) // multiplier)
        x_end = min(max_x, end // multiplier)

        for x in range(x_start, x_end + 1):
            invalid_id = x * multiplier
            if start <= invalid_id <= end:
                invalid_ids.append(invalid_id)

        n += 1

    return invalid_ids


def solve_part1(input_text: str) -> int:
    """Find and sum all invalid IDs in the given ranges."""
    line = input_text.strip()
    ranges = line.split(',')

    total = 0
    for r in ranges:
        parts = r.split('-')
        start = int(parts[0])
        end = int(parts[1])
        invalid_ids = generate_invalid_ids_in_range(start, end)
        total += sum(invalid_ids)

    return total


def generate_invalid_ids_part2_in_range(start: int, end: int) -> set[int]:
    """Generate all invalid IDs (repeated at least twice) in range [start, end]."""
    invalid_ids: set[int] = set()

    # For pattern length n and repetition count k >= 2
    # Total length L = n * k
    # Multiplier M = (10^(n*k) - 1) / (10^n - 1)

    n = 1
    while True:
        base_min = 10**(n-1) if n > 1 else 1
        base_max = 10**n - 1

        # Smallest possible ID with pattern length n is base_min repeated twice
        # Multiplier for k=2 is 10^n + 1
        smallest_id = base_min * (10**n + 1)
        if smallest_id > end:
            break

        k = 2
        while True:
            total_len = n * k
            # Multiplier = (10^(n*k) - 1) / (10^n - 1)
            multiplier = (10**(n*k) - 1) // (10**n - 1)

            min_id = base_min * multiplier
            max_id = base_max * multiplier

            if min_id > end:
                break

            x_start = max(base_min, (start + multiplier - 1) // multiplier)
            x_end = min(base_max, end // multiplier)

            for x in range(x_start, x_end + 1):
                invalid_id = x * multiplier
                if start <= invalid_id <= end:
                    invalid_ids.add(invalid_id)

            k += 1

        n += 1

    return invalid_ids


def solve_part2(input_text: str) -> int:
    """Find and sum all invalid IDs (repeated at least twice) in the given ranges."""
    line = input_text.strip()
    ranges = line.split(',')

    total = 0
    for r in ranges:
        parts = r.split('-')
        start = int(parts[0])
        end = int(parts[1])
        invalid_ids = generate_invalid_ids_part2_in_range(start, end)
        total += sum(invalid_ids)

    return total


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python problem.py <input_file>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        input_text = f.read()

    print(solve_part1(input_text))
    print(solve_part2(input_text))


if __name__ == "__main__":
    main()
