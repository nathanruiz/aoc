import sys
import re

def main():
    pattern = re.compile(r"mul\((\d+),(\d+)\)")

    input_memory = sys.stdin.read()
    total = 0
    for match in pattern.finditer(input_memory):
        a, b = match.groups()
        total += int(a) * int(b)

    print(f"[Part one] Result {total}")

if __name__ == "__main__":
    main()
