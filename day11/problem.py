#!/usr/bin/env python3
import sys
from collections import defaultdict, deque


def parse_input(filename: str) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = defaultdict(list)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(": ")
            source = parts[0]
            if len(parts) > 1:
                destinations = parts[1].split()
                graph[source] = destinations
    return graph


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    all_nodes: set[str] = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)

    in_degree: dict[str, int] = {node: 0 for node in all_nodes}
    for neighbors in graph.values():
        for neighbor in neighbors:
            in_degree[neighbor] += 1

    queue = deque([node for node in all_nodes if in_degree[node] == 0])
    result: list[str] = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result


def count_paths_dag(graph: dict[str, list[str]], start: str, end: str) -> int:
    topo_order = topological_sort(graph)
    dp: dict[str, int] = defaultdict(int)
    dp[end] = 1

    for node in reversed(topo_order):
        if node == end:
            continue
        for neighbor in graph.get(node, []):
            dp[node] += dp[neighbor]

    return dp[start]


def count_paths_with_required_dag(
    graph: dict[str, list[str]], start: str, end: str, required: set[str]
) -> int:
    req_list = list(required)
    n_req = len(req_list)
    full_mask = (1 << n_req) - 1

    def get_mask(node: str) -> int:
        mask = 0
        for i, req in enumerate(req_list):
            if node == req:
                mask |= (1 << i)
        return mask

    topo_order = topological_sort(graph)

    dp: dict[tuple[str, int], int] = defaultdict(int)
    dp[(start, get_mask(start))] = 1

    for node in topo_order:
        for mask in range(full_mask + 1):
            if dp[(node, mask)] == 0:
                continue

            for neighbor in graph.get(node, []):
                new_mask = mask | get_mask(neighbor)
                dp[(neighbor, new_mask)] += dp[(node, mask)]

    return dp[(end, full_mask)]


def solve_part1(filename: str) -> int:
    graph = parse_input(filename)
    return count_paths_dag(graph, "you", "out")


def solve_part2(filename: str) -> int:
    graph = parse_input(filename)
    return count_paths_with_required_dag(graph, "svr", "out", {"dac", "fft"})


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python problem.py <input_file>")
        sys.exit(1)

    filename = sys.argv[1]
    print(solve_part1(filename))
    print(solve_part2(filename))


if __name__ == "__main__":
    main()
