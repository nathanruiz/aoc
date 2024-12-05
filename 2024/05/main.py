import sys
from collections import defaultdict

class OrderingRuleChecker:
    ordering_rules: dict[int, set[int]]
    reverse_rules: dict[int, set[int]]

    def __init__(self, ordering_rules: dict[int, set[int]]) -> None:
        self.ordering_rules = ordering_rules

    def is_ordered(self, values: list[int]) -> bool:
        for i, value in enumerate(values):
            for after in values[i+1:]:
                if after not in self.ordering_rules[value]:
                    return False
        return True

    def reorder(self, values: list[int]) -> list[int]:
        result = []
        values = set(values)
        while values:
            for value in values:
                # Find the value that has all other values on the right side.
                if values - self.ordering_rules[value] == {value}:
                    result.append(value)
                    values.remove(value)
                    break
        return result

def main():
    ordering_rules = defaultdict(set)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        before, after = line.split("|")
        ordering_rules[int(before)].add(int(after))

    checker = OrderingRuleChecker(ordering_rules)
    correct_results = 0
    fixed_results = 0
    for line in sys.stdin:
        line = line.strip()
        values = [int(value) for value in line.split(",")]
        if checker.is_ordered(values):
            correct_results += values[int(len(values)/2)]
        else:
            values = checker.reorder(values)
            fixed_results += values[int(len(values)/2)]

    print(f"[Part one] Correct result {correct_results}")
    print(f"[Part two] Fixed result {fixed_results}")


if __name__ == "__main__":
    main()
