import sys
from itertools import product

def main():
    lines = [line.strip() for line in sys.stdin.readlines()]

    result = 0
    for line in lines:
        expected, inputs = line.split(": ")
        expected = int(expected)
        inputs = [int(value) for value in inputs.split()]
        if is_valid_equation(expected, inputs, ["+", "*"]):
            result += expected

    print(f"[Part one] Calibration results {result}")


def is_valid_equation(expected: int, inputs: list[str], operators: list[str]) -> bool:
    for operators in product(operators, repeat=len(inputs) - 1):
        values = list(reversed(inputs))
        for operator in operators:
            b = values.pop()
            a = values.pop()
            if operator == "+":
                values.append(a + b)
            elif operator == "*":
                values.append(a * b)

        if values[0] == expected:
            return True

if __name__ == "__main__":
    main()
