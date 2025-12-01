#!/usr/bin/env python3
import sys


def count_zeros_left(start: int, distance: int) -> int:
    first_k = start if start > 0 else 100
    if first_k > distance:
        return 0
    return (distance - first_k) // 100 + 1


def count_zeros_right(start: int, distance: int) -> int:
    first_k = (100 - start) % 100
    if first_k == 0:
        first_k = 100
    if first_k > distance:
        return 0
    return (distance - first_k) // 100 + 1


def solve_part1(input_text: str) -> int:
    position = 50
    count = 0

    for line in input_text.strip().split('\n'):
        direction = line[0]
        distance = int(line[1:])

        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100

        if position == 0:
            count += 1

    return count


def solve_part2(input_text: str) -> int:
    position = 50
    count = 0

    for line in input_text.strip().split('\n'):
        direction = line[0]
        distance = int(line[1:])

        if direction == 'L':
            count += count_zeros_left(position, distance)
            position = (position - distance) % 100
        else:
            count += count_zeros_right(position, distance)
            position = (position + distance) % 100

    return count


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
