import sys
from dataclasses import dataclass

@dataclass(frozen=True)
class Range:
    start: int
    end: int

    def __contains__(self, ingredient_id: int) -> bool:
        return self.start <= ingredient_id and ingredient_id <= self.end

    def overlaps(self, other: "Range") -> bool:
        return self.start <= other.end and other.start <= self.end

    def merge(self, other: "Range") -> "Range":
        if not self.overlaps(other):
            raise ValueError("Unable to merge non-contiguous ranges")

        start = min(self.start, other.start)
        end = max(self.end, other.end)
        return Range(start, end)

    def __len__(self) -> int:
        return self.end - self.start + 1


def main():
    fresh_ranges: list[Range] = []
    for line in sys.stdin:
        if line.strip() == "":
            break
        start, end = line.strip().split("-")
        fresh_ranges.append(Range(int(start), int(end)))

    ingredients: list[int] = []
    for line in sys.stdin:
        ingredients.append(int(line.strip()))

    fresh_count = 0
    for ingredient in ingredients:
        for fresh_range in fresh_ranges:
            if ingredient in fresh_range:
                fresh_count += 1
                break

    print(f"[Part one] Number of fresh ingredients {fresh_count}")

    merged_ranges = set()
    for fresh_range in fresh_ranges:
        for next_range in list(merged_ranges):
            if fresh_range.overlaps(next_range):
                merged_ranges.remove(next_range)
                fresh_range = fresh_range.merge(next_range)

        merged_ranges.add(fresh_range)

    fresh_ids = sum(len(fresh_range) for fresh_range in merged_ranges)
    print(f"[Part two] Number of fresh IDs {fresh_ids}")

if __name__ == "__main__":
    main()
