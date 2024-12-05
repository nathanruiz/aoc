import sys
from collections import defaultdict

class OrderingRuleChecker:
    ordering_rules: dict[int, set[int]]

    def __init__(self, ordering_rules: dict[int, set[int]]):
        self.ordering_rules = ordering_rules

    def is_ordered(self, values: list[int]):
        for i, value in enumerate(values):
            for after in values[i+1:]:
                if after not in self.ordering_rules[value]:
                    return False
        return True

def main():
    ordering_rules = defaultdict(set)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        before, after = line.split("|")
        ordering_rules[int(before)].add(int(after))

    checker = OrderingRuleChecker(ordering_rules)
    result = 0
    for line in sys.stdin:
        line = line.strip()
        values = [int(value) for value in line.split(",")]
        if checker.is_ordered(values):
            result += values[int(len(values)/2)]

    print(f"[Part one] Result {result}")


if __name__ == "__main__":
    main()
