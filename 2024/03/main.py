import sys
import re

def main():
    input_memory = sys.stdin.read()

    part_one(input_memory)
    part_two(input_memory)

def part_one(input_memory):
    pattern = re.compile(r"mul\((\d+),(\d+)\)")

    total = 0
    for match in pattern.finditer(input_memory):
        a, b = match.groups()
        total += int(a) * int(b)

    print(f"[Part one] Result {total}")

def part_two(input_memory):
    pattern = re.compile(r"(mul|do|don't)\(((\d+),(\d+)|)\)")

    total = 0
    multiply_enabled = True
    for match in pattern.finditer(input_memory):
        op = match.group(1)
        if op == "mul":
            if multiply_enabled:
                _, _, a, b = match.groups()
                total += int(a) * int(b)
        elif op == "do":
            multiply_enabled = True
        elif op == "don't":
            multiply_enabled = False

    print(f"[Part two] Result {total}")


if __name__ == "__main__":
    main()
