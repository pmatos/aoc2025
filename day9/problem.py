#!/usr/bin/env python3
import sys
from typing import List, Tuple, Set


def parse_input(filename: str) -> List[Tuple[int, int]]:
    tiles: List[Tuple[int, int]] = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = line.split(",")
                tiles.append((int(x), int(y)))
    return tiles


def find_largest_rectangle(tiles: List[Tuple[int, int]]) -> int:
    max_area = 0
    n = len(tiles)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area > max_area:
                max_area = area
    return max_area


def build_green_tiles(red_tiles: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    green: Set[Tuple[int, int]] = set()
    n = len(red_tiles)
    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if (x1, y) not in [(x1, y1), (x2, y2)]:
                    green.add((x1, y))
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if (x, y1) not in [(x1, y1), (x2, y2)]:
                    green.add((x, y1))
    return green


def get_polygon_edges(
    red_tiles: List[Tuple[int, int]]
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    edges: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    n = len(red_tiles)
    for i in range(n):
        edges.append((red_tiles[i], red_tiles[(i + 1) % n]))
    return edges


def fill_polygon_interior(
    red_tiles: List[Tuple[int, int]], boundary: Set[Tuple[int, int]]
) -> Set[Tuple[int, int]]:
    all_points = set(red_tiles) | boundary
    if not all_points:
        return set()

    min_x = min(p[0] for p in all_points)
    max_x = max(p[0] for p in all_points)
    min_y = min(p[1] for p in all_points)
    max_y = max(p[1] for p in all_points)

    edges = get_polygon_edges(red_tiles)
    interior: Set[Tuple[int, int]] = set()

    for y in range(min_y, max_y + 1):
        crossings: List[float] = []
        for (x1, y1), (x2, y2) in edges:
            if y1 == y2:
                continue
            if min(y1, y2) <= y < max(y1, y2):
                x_cross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                crossings.append(x_cross)
        crossings.sort()

        for i in range(0, len(crossings) - 1, 2):
            x_start = int(crossings[i])
            x_end = int(crossings[i + 1])
            for x in range(x_start, x_end + 1):
                if (x, y) not in all_points:
                    interior.add((x, y))

    return interior


def get_y_intervals_at_x(
    x: int, edges: List[Tuple[Tuple[int, int], Tuple[int, int]]]
) -> List[Tuple[int, int]]:
    crossings: List[int] = []
    for (x1, y1), (x2, y2) in edges:
        if x1 == x2:
            continue
        if min(x1, x2) <= x < max(x1, x2):
            y_cross = y1 + (x - x1) * (y2 - y1) // (x2 - x1)
            crossings.append(y_cross)
    crossings.sort()
    intervals: List[Tuple[int, int]] = []
    for i in range(0, len(crossings) - 1, 2):
        intervals.append((crossings[i], crossings[i + 1]))
    return intervals


def point_in_polygon(
    x: int,
    y: int,
    edges: List[Tuple[Tuple[int, int], Tuple[int, int]]],
) -> bool:
    for (x1, y1), (x2, y2) in edges:
        if y1 == y2 == y and min(x1, x2) <= x <= max(x1, x2):
            return True
        if x1 == x2 == x and min(y1, y2) <= y <= max(y1, y2):
            return True

    crossings = 0
    for (x1, y1), (x2, y2) in edges:
        if y1 == y2:
            continue
        if min(y1, y2) <= y < max(y1, y2):
            x_cross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x_cross > x:
                crossings += 1

    return crossings % 2 == 1


def is_rectangle_valid(
    min_x: int,
    max_x: int,
    min_y: int,
    max_y: int,
    edges: List[Tuple[Tuple[int, int], Tuple[int, int]]],
) -> bool:
    corners = [
        (min_x, min_y),
        (min_x, max_y),
        (max_x, min_y),
        (max_x, max_y),
    ]
    for cx, cy in corners:
        if not point_in_polygon(cx, cy, edges):
            return False

    for (x1, y1), (x2, y2) in edges:
        if x1 == x2:
            if min_x < x1 < max_x:
                edge_min_y, edge_max_y = min(y1, y2), max(y1, y2)
                if edge_min_y < min_y < edge_max_y or edge_min_y < max_y < edge_max_y:
                    return False
                if min_y < edge_min_y and edge_max_y < max_y:
                    return False
        else:
            if min_y < y1 < max_y:
                edge_min_x, edge_max_x = min(x1, x2), max(x1, x2)
                if edge_min_x < min_x < edge_max_x or edge_min_x < max_x < edge_max_x:
                    return False
                if min_x < edge_min_x and edge_max_x < max_x:
                    return False

    return True


def find_largest_valid_rectangle(red_tiles: List[Tuple[int, int]]) -> int:
    edges = get_polygon_edges(red_tiles)

    max_area = 0
    n = len(red_tiles)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)

            area = (max_x - min_x + 1) * (max_y - min_y + 1)
            if area <= max_area:
                continue

            if is_rectangle_valid(min_x, max_x, min_y, max_y, edges):
                max_area = area

    return max_area


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python problem.py <input_file>")
        sys.exit(1)

    tiles = parse_input(sys.argv[1])
    result1 = find_largest_rectangle(tiles)
    print(result1)
    result2 = find_largest_valid_rectangle(tiles)
    print(result2)


if __name__ == "__main__":
    main()
