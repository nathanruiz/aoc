import sys
from itertools import product

def main():
    lines = []
    for line in sys.stdin:
        expected, inputs = line.strip().split(": ")
        expected = int(expected)
        inputs = [int(value) for value in inputs.split()]
        lines.append((expected, inputs))

    result = sum(
        expected
        for expected, inputs in lines
        if is_valid_equation(expected, inputs, ["+", "*"])
    )
    print(f"[Part one] Calibration results {result}")

    result = sum(
        expected
        for expected, inputs in lines
        if is_valid_equation(expected, inputs, ["+", "*", "||"])
    )
    print(f"[Part two] Calibration results {result}")

def is_valid_equation(expected: int, inputs: list[str], operators: list[str]) -> bool:
    for operators in product(operators, repeat=len(inputs) - 1):
        values = list(reversed(inputs))
        for operator in operators:
            a = values.pop()
            b = values.pop()
            if operator == "+":
                values.append(a + b)
            elif operator == "*":
                values.append(a * b)
            elif operator == "||":
                values.append(int(str(a) + str(b)))

        if values[0] == expected:
            return True

if __name__ == "__main__":
    main()
