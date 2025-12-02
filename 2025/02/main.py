import itertools
import sys
from typing import Generator

class IDRange:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def get_pairs(self) -> Generator[int, None, None]:
        for i in range(self.start, self.end + 1):
            i_str = str(i)
            if len(i_str) % 2 != 0:
                continue

            pivot = len(i_str) // 2
            if i_str[pivot:] == i_str[:pivot]:
                yield i

    def get_repeated(self) -> Generator[int, None, None]:
        for i in range(self.start, self.end + 1):
            i_str = str(i)

            for divisor in range(1, len(i_str)):
                if len(i_str) % divisor != 0:
                    continue

                if self.is_repeated(i_str, divisor):
                    yield i
                    break

    @classmethod
    def is_repeated(cls, value: str, divisor: int) -> bool:
        chunks = list(itertools.batched(value, divisor))
        for chunk in chunks[1:]:
            if chunks[0] != chunk:
                return False
        return True


def part1(ranges: list[str]):
    invalid_sum = sum(sum(id_range.get_pairs()) for id_range in ranges)
    print(f"[Part One] Invalid sum {invalid_sum}")


def part2(ranges: list[str]):
    invalid_sum = sum(sum(id_range.get_repeated()) for id_range in ranges)
    print(f"[Part Two] Invalid sum {invalid_sum}")


def main():
    ranges = []
    for id_range_str in sys.stdin.read().split(","):
        start, end = id_range_str.split("-")
        ranges.append(IDRange(int(start), int(end)))

    part1(ranges)
    part2(ranges)

if __name__ == "__main__":
    main()
