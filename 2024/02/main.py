from collections import defaultdict
from typing import List
from enum import Enum
from itertools import pairwise
from unittest import TestCase

class Direction(Enum):
    UP = 1
    DOWN = -1

def main():
    safe_count = 0
    unsafe_count = 0
    with open("input") as input:
        for line in input:
            report = [int(level) for level in line.split()]
            if is_safe_report(report):
                safe_count += 1
            else:
                unsafe_count += 1

        print(f"[Part one] {safe_count} safe reports, {unsafe_count} unsafe reports")

def is_safe_report(report: List[int]) -> bool:
    direction = Direction.UP if report[0] < report[1] else Direction.DOWN
    return all(
        is_safe_increment(previous, current, direction)
        for previous, current in pairwise(report)
    )

def is_safe_increment(previous: int, current: int, direction: Direction) -> bool:
    diff = (current - previous) * direction.value
    return diff >= 1 and diff <= 3

class IsSafeIncrementTestCase(TestCase):
    def test_going_up(self):
        self.assertTrue(is_safe_increment(10, 12, Direction.UP))

    def test_going_down(self):
        self.assertTrue(is_safe_increment(12, 10, Direction.DOWN))

    def test_going_up_too_much(self):
        self.assertFalse(is_safe_increment(10, 14, Direction.UP))

    def test_going_down_too_much(self):
        self.assertFalse(is_safe_increment(14, 10, Direction.DOWN))

    def test_wrong_direction(self):
        self.assertFalse(is_safe_increment(10, 14, Direction.DOWN))
        self.assertFalse(is_safe_increment(14, 10, Direction.UP))

    def test_unchanged(self):
        self.assertFalse(is_safe_increment(10, 10, Direction.DOWN))
        self.assertFalse(is_safe_increment(10, 10, Direction.UP))

    def test_bounds(self):
        self.assertFalse(is_safe_increment(10, 10, Direction.UP))
        self.assertTrue(is_safe_increment(10, 11, Direction.UP))
        self.assertTrue(is_safe_increment(10, 13, Direction.UP))
        self.assertFalse(is_safe_increment(10, 14, Direction.UP))

class IsSafeReportTestCase(TestCase):
    def test_safe_reports(self):
        # Safe because the levels are all decreasing by 1 or 2.
        self.assertTrue(is_safe_report([7, 6, 4, 2, 1]))

        # Safe because the levels are all increasing by 1, 2, or 3.
        self.assertTrue(is_safe_report([1, 3, 6, 7, 9]))

    def test_too_much(self):
        # Unsafe because 2 7 is an increase of 5.
        self.assertFalse(is_safe_report([1, 2, 7, 8, 9]))

        # Unsafe because 6 2 is a decrease of 4.
        self.assertFalse(is_safe_report([9, 7, 6, 2, 1]))

    def test_wrong_direction(self):
        # Unsafe because 1 3 is increasing but 3, 2 is decreasing.
        self.assertFalse(is_safe_report([1, 3, 2, 4, 5]))

    def test_unchanged(self):
        # Unsafe because 4 4 is neither an increase or a decrease.
        self.assertFalse(is_safe_report([8, 6, 4, 4, 1]))


if __name__ == "__main__":
    main()
