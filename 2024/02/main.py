from enum import Enum
from itertools import pairwise
from typing import List
from unittest import TestCase
import sys

class Direction(Enum):
    UP = 1
    DOWN = -1

class ReportChecker:
    safe: int
    unsafe: int

    def __init__(self):
        self.safe = 0
        self.unsafe = 0

    def check_report(self, report: List[int]):
        if self.is_safe_report(report):
            self.safe += 1
        else:
            self.unsafe += 1

    def is_safe_report(self, report: List[int]) -> bool:
        direction = Direction.UP if report[0] < report[1] else Direction.DOWN
        return all(
            self.is_safe_increment(previous, current, direction)
            for previous, current in pairwise(report)
        )

    def is_safe_increment(self, previous: int, current: int, direction: Direction) -> bool:
        diff = (current - previous) * direction.value
        return diff >= 1 and diff <= 3

class ProblemDampenerReportChecker(ReportChecker):
    def is_safe_report(self, report: List[int]) -> bool:
        for i in range(len(report)):
            if super().is_safe_report(report[:i] + report[i + 1:]):
                return True
        return False

def main():
    report_checker = ReportChecker()
    problem_dampener_report_checker = ProblemDampenerReportChecker()

    for line in sys.stdin:
        report = [int(level) for level in line.split()]
        report_checker.check_report(report)
        problem_dampener_report_checker.check_report(report)

    print(f"[Part one] {report_checker.safe} safe reports, {report_checker.unsafe} unsafe reports")
    print(
        f"[Part two] {problem_dampener_report_checker.safe} safe reports, "
        f"{problem_dampener_report_checker.unsafe} unsafe reports"
    )


class IsSafeIncrementTestCase(TestCase):
    def setUp(self):
        self.checker = ReportChecker()

    def test_going_up(self):
        self.assertTrue(self.checker.is_safe_increment(10, 12, Direction.UP))

    def test_going_down(self):
        self.assertTrue(self.checker.is_safe_increment(12, 10, Direction.DOWN))

    def test_going_up_too_much(self):
        self.assertFalse(self.checker.is_safe_increment(10, 14, Direction.UP))

    def test_going_down_too_much(self):
        self.assertFalse(self.checker.is_safe_increment(14, 10, Direction.DOWN))

    def test_wrong_direction(self):
        self.assertFalse(self.checker.is_safe_increment(10, 14, Direction.DOWN))
        self.assertFalse(self.checker.is_safe_increment(14, 10, Direction.UP))

    def test_unchanged(self):
        self.assertFalse(self.checker.is_safe_increment(10, 10, Direction.DOWN))
        self.assertFalse(self.checker.is_safe_increment(10, 10, Direction.UP))

    def test_bounds(self):
        self.assertFalse(self.checker.is_safe_increment(10, 10, Direction.UP))
        self.assertTrue(self.checker.is_safe_increment(10, 11, Direction.UP))
        self.assertTrue(self.checker.is_safe_increment(10, 13, Direction.UP))
        self.assertFalse(self.checker.is_safe_increment(10, 14, Direction.UP))

class IsSafeReportTestCase(TestCase):
    def setUp(self):
        self.checker = ReportChecker()

    def test_safe_reports(self):
        # Safe because the levels are all decreasing by 1 or 2.
        self.assertTrue(self.checker.is_safe_report([7, 6, 4, 2, 1]))

        # Safe because the levels are all increasing by 1, 2, or 3.
        self.assertTrue(self.checker.is_safe_report([1, 3, 6, 7, 9]))

    def test_too_much(self):
        # Unsafe because 2 7 is an increase of 5.
        self.assertFalse(self.checker.is_safe_report([1, 2, 7, 8, 9]))

        # Unsafe because 6 2 is a decrease of 4.
        self.assertFalse(self.checker.is_safe_report([9, 7, 6, 2, 1]))

    def test_wrong_direction(self):
        # Unsafe because 1 3 is increasing but 3, 2 is decreasing.
        self.assertFalse(self.checker.is_safe_report([1, 3, 2, 4, 5]))

    def test_unchanged(self):
        # Unsafe because 4 4 is neither an increase or a decrease.
        self.assertFalse(self.checker.is_safe_report([8, 6, 4, 4, 1]))

class IsProblemDampenerSafeReportTestCase(TestCase):
    def setUp(self):
        self.checker = ProblemDampenerReportChecker()

    def test_safe(self):
        # Safe without removing any level.
        self.assertTrue(self.checker.is_safe_report([7, 6, 4, 2, 1]))

        # Safe by removing the second level, 3.
        self.assertTrue(self.checker.is_safe_report([1, 3, 2, 4, 5]))

        # Safe by removing the third level, 4.
        self.assertTrue(self.checker.is_safe_report([8, 6, 4, 4, 1]))

        # Safe without removing any level.
        self.assertTrue(self.checker.is_safe_report([1, 3, 6, 7, 9]))

        # Safe without removing any level.
        self.assertTrue(self.checker.is_safe_report([1, 9, 2, 3, 4]))

    def test_unsafe(self):
        # Unsafe regardless of which level is removed.
        self.assertFalse(self.checker.is_safe_report([1, 2, 7, 8, 9]))

        # Unsafe regardless of which level is removed.
        self.assertFalse(self.checker.is_safe_report([9, 7, 6, 2, 1]))

if __name__ == "__main__":
    main()
