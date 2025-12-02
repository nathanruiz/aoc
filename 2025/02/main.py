import sys
from typing import Generator

class IDRange:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def invalid_values(self) -> Generator[int, None, None]:
        for i in range(self.start, self.end + 1):
            i_str = str(i)
            if len(i_str) % 2 != 0:
                continue

            pivot = len(i_str) // 2
            if i_str[pivot:] == i_str[:pivot]:
                yield i

def part1(ranges: list[str]):
    invalid_sum = 0
    for id_range_str in ranges:
        start, end = id_range_str.split("-")
        id_range = IDRange(int(start), int(end))
        invalid_sum += sum(id_range.invalid_values())

    print(f"[Part One] Invalid sum {invalid_sum}")


def main():
    ranges = sys.stdin.read().split(",")
    part1(ranges)

if __name__ == "__main__":
    main()
