#!/usr/bin/env python3
import sys
from typing import TextIO


def parse_input(f: TextIO) -> list[tuple[int, int, int]]:
    points: list[tuple[int, int, int]] = []
    for line in f:
        line = line.strip()
        if line:
            x, y, z = map(int, line.split(','))
            points.append((x, y, z))
    return points


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.num_components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.num_components -= 1
        return True

    def get_component_sizes(self) -> list[int]:
        sizes: list[int] = []
        for i in range(len(self.parent)):
            if self.find(i) == i:
                sizes.append(self.size[i])
        return sizes


def euclidean_distance_sq(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> int:
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2


def get_all_pairs_sorted(points: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    n = len(points)
    pairs: list[tuple[int, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            dist_sq = euclidean_distance_sq(points[i], points[j])
            pairs.append((dist_sq, i, j))
    pairs.sort()
    return pairs


def part1(points: list[tuple[int, int, int]]) -> int:
    n = len(points)
    uf = UnionFind(n)

    pairs = get_all_pairs_sorted(points)

    for _, i, j in pairs[:1000]:
        uf.union(i, j)

    sizes = uf.get_component_sizes()
    sizes.sort(reverse=True)

    return sizes[0] * sizes[1] * sizes[2]


def part2(points: list[tuple[int, int, int]]) -> int:
    n = len(points)
    uf = UnionFind(n)

    pairs = get_all_pairs_sorted(points)

    for _, i, j in pairs:
        if uf.union(i, j):
            if uf.num_components == 1:
                return points[i][0] * points[j][0]

    return 0


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_file>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        points = parse_input(f)

    result1 = part1(points)
    print(result1)

    result2 = part2(points)
    print(result2)


if __name__ == "__main__":
    main()
