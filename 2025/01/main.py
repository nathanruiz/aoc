import sys


def main():
    position = 50
    password = 0
    for line in sys.stdin:
        line = line.strip()
        if line[0] == "R":
            position += int(line[1:])
        elif line[0] == "L":
            position -= int(line[1:])
        else:
            raise ValueError(f"Invalid instruction {line}")
        position %= 100

        if position == 0:
            password += 1

    print(f"[Part One] Password is {password}")


if __name__ == "__main__":
    main()
