#!/usr/bin/env python3
import sys
import re
from itertools import combinations
from fractions import Fraction


def parse_line(line: str) -> tuple[list[bool], list[list[int]], list[int]]:
    """Parse a machine line into target configuration, button wirings, and joltage."""
    target_match = re.match(r'\[([.#]+)\]', line)
    if not target_match:
        raise ValueError(f"Could not parse target from line: {line}")

    target_str = target_match.group(1)
    target = [c == '#' for c in target_str]

    button_pattern = r'\(([0-9,]+)\)'
    buttons = []
    for match in re.finditer(button_pattern, line):
        indices = [int(x) for x in match.group(1).split(',')]
        buttons.append(indices)

    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage: list[int] = []
    if joltage_match:
        joltage = [int(x) for x in joltage_match.group(1).split(',')]

    return target, buttons, joltage


def apply_buttons(n_lights: int, buttons: list[list[int]], pressed: list[int]) -> list[bool]:
    """Apply button presses and return resulting light configuration."""
    state = [False] * n_lights
    for btn_idx in pressed:
        for light_idx in buttons[btn_idx]:
            state[light_idx] = not state[light_idx]
    return state


def min_presses_bruteforce(target: list[bool], buttons: list[list[int]]) -> int:
    """Find minimum button presses using brute force."""
    n_lights = len(target)
    n_buttons = len(buttons)

    for num_presses in range(n_buttons + 1):
        for combo in combinations(range(n_buttons), num_presses):
            state = apply_buttons(n_lights, buttons, list(combo))
            if state == target:
                return num_presses

    return -1


def solve_gf2(target: list[bool], buttons: list[list[int]]) -> int:
    """
    Solve using Gaussian elimination over GF(2).
    Returns minimum number of buttons to press.
    """
    n_lights = len(target)
    n_buttons = len(buttons)

    if n_buttons == 0:
        return 0 if all(not t for t in target) else -1

    matrix: list[list[int]] = []
    for light in range(n_lights):
        row = [1 if light in buttons[btn] else 0 for btn in range(n_buttons)]
        row.append(1 if target[light] else 0)
        matrix.append(row)

    rows = len(matrix)
    cols = n_buttons

    pivot_row = 0
    pivot_cols: list[int] = []

    for col in range(cols):
        found = -1
        for row in range(pivot_row, rows):
            if matrix[row][col] == 1:
                found = row
                break

        if found == -1:
            continue

        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        pivot_cols.append(col)

        for row in range(rows):
            if row != pivot_row and matrix[row][col] == 1:
                for c in range(cols + 1):
                    matrix[row][c] ^= matrix[pivot_row][c]

        pivot_row += 1

    for row in range(pivot_row, rows):
        if matrix[row][cols] == 1:
            return -1

    free_vars = [c for c in range(cols) if c not in pivot_cols]
    n_free = len(free_vars)

    min_presses = float('inf')

    for free_assignment in range(1 << n_free):
        solution = [0] * cols

        for i, col in enumerate(free_vars):
            solution[col] = (free_assignment >> i) & 1

        for i in range(len(pivot_cols) - 1, -1, -1):
            pcol = pivot_cols[i]
            val = matrix[i][cols]
            for c in range(pcol + 1, cols):
                val ^= matrix[i][c] * solution[c]
            solution[pcol] = val

        presses = sum(solution)
        min_presses = min(min_presses, presses)

    return int(min_presses)


def solve_part1(lines: list[str]) -> int:
    """Solve part 1 - minimum total button presses."""
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        target, buttons, _ = parse_line(line)
        presses = solve_gf2(target, buttons)
        if presses == -1:
            presses = min_presses_bruteforce(target, buttons)
        total += presses
    return total


def solve_joltage_ilp(joltage: list[int], buttons: list[list[int]]) -> int:
    """
    Solve joltage problem using Gaussian elimination over rationals,
    then enumerate free variables to minimize total presses.
    """
    n_counters = len(joltage)
    n_buttons = len(buttons)

    if n_buttons == 0:
        return 0 if all(j == 0 for j in joltage) else -1

    matrix: list[list[Fraction]] = []
    for counter in range(n_counters):
        row = [Fraction(1) if counter in buttons[btn] else Fraction(0) for btn in range(n_buttons)]
        row.append(Fraction(joltage[counter]))
        matrix.append(row)

    rows = len(matrix)
    cols = n_buttons

    pivot_row = 0
    pivot_cols: list[int] = []

    for col in range(cols):
        found = -1
        for row in range(pivot_row, rows):
            if matrix[row][col] != 0:
                found = row
                break

        if found == -1:
            continue

        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        pivot_cols.append(col)

        pivot_val = matrix[pivot_row][col]
        for c in range(cols + 1):
            matrix[pivot_row][c] /= pivot_val

        for row in range(rows):
            if row != pivot_row and matrix[row][col] != 0:
                factor = matrix[row][col]
                for c in range(cols + 1):
                    matrix[row][c] -= factor * matrix[pivot_row][c]

        pivot_row += 1

    for row in range(pivot_row, rows):
        if matrix[row][cols] != 0:
            return -1

    free_vars = [c for c in range(cols) if c not in pivot_cols]
    n_free = len(free_vars)

    if n_free == 0:
        solution = [Fraction(0)] * cols
        for i, pcol in enumerate(pivot_cols):
            solution[pcol] = matrix[i][cols]

        for s in solution:
            if s < 0 or s.denominator != 1:
                return -1
        return sum(int(s) for s in solution)

    max_free_val = max(joltage) + 1

    min_presses = float('inf')

    def search(free_idx: int, free_vals: list[int], current_sum: int) -> None:
        nonlocal min_presses

        if current_sum >= min_presses:
            return

        if free_idx == n_free:
            solution = [Fraction(0)] * cols
            for i, col in enumerate(free_vars):
                solution[col] = Fraction(free_vals[i])

            for i in range(len(pivot_cols) - 1, -1, -1):
                pcol = pivot_cols[i]
                val = matrix[i][cols]
                for c in range(pcol + 1, cols):
                    val -= matrix[i][c] * solution[c]
                solution[pcol] = val

            valid = all(s >= 0 and s.denominator == 1 for s in solution)
            if valid:
                total = sum(int(s) for s in solution)
                min_presses = min(min_presses, total)
            return

        for val in range(max_free_val):
            search(free_idx + 1, free_vals + [val], current_sum + val)

    search(0, [], 0)

    return int(min_presses) if min_presses != float('inf') else -1


def solve_part2(lines: list[str]) -> int:
    """Solve part 2 - minimum total button presses for joltage."""
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        _, buttons, joltage = parse_line(line)
        presses = solve_joltage_ilp(joltage, buttons)
        if presses == -1:
            raise ValueError(f"No solution found for line: {line}")
        total += presses
    return total


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python problem.py <input_file>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    result1 = solve_part1(lines)
    print(result1)

    result2 = solve_part2(lines)
    print(result2)


if __name__ == "__main__":
    main()
