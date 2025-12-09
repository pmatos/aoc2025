#!/usr/bin/env python3
import tempfile
import os
from problem import (
    parse_input,
    find_largest_rectangle,
    find_largest_valid_rectangle,
    build_green_tiles,
    fill_polygon_interior,
)


def test_example() -> None:
    example_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(example_data)
        f.flush()
        tiles = parse_input(f.name)
        result = find_largest_rectangle(tiles)
        os.unlink(f.name)
    assert result == 50, f"Expected 50, got {result}"


def test_parse_input() -> None:
    example_data = """7,1
11,1
11,7"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(example_data)
        f.flush()
        tiles = parse_input(f.name)
        os.unlink(f.name)
    assert tiles == [(7, 1), (11, 1), (11, 7)]


def test_simple_rectangle() -> None:
    example_data = """0,0
10,5"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(example_data)
        f.flush()
        tiles = parse_input(f.name)
        result = find_largest_rectangle(tiles)
        os.unlink(f.name)
    # Area is (10-0+1) * (5-0+1) = 11 * 6 = 66
    assert result == 66, f"Expected 66, got {result}"


def test_part2_example() -> None:
    example_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(example_data)
        f.flush()
        tiles = parse_input(f.name)
        result = find_largest_valid_rectangle(tiles)
        os.unlink(f.name)
    assert result == 24, f"Expected 24, got {result}"


def test_green_tiles() -> None:
    tiles = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
    green = build_green_tiles(tiles)
    assert (8, 1) in green
    assert (9, 1) in green
    assert (10, 1) in green
    assert (11, 2) in green


if __name__ == "__main__":
    test_parse_input()
    test_example()
    test_simple_rectangle()
    test_green_tiles()
    test_part2_example()
    print("All tests passed!")
