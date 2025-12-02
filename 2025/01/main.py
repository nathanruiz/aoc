import sys

def main():
    lines = sys.stdin.readlines()
    part1(lines)
    part2(lines)

def part1(lines):
    position = 50
    password = 0

    for line in lines:
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

def part2(lines):
    position = 50
    password = 0

    for line in lines:
        line = line.strip()
        if line[0] == "R":
            # If we are turning right, any change in digits above the hundreds
            # indicates we are going over the zero position again.
            initial_iterations = position // 100
            position += int(line[1:])
            new_iterations = position // 100
            password += new_iterations - initial_iterations
        elif line[0] == "L":
            # If we are turning left, we follow the same rule unless the
            # starting or ending position is exactly zero. Moving to the ending
            # position of zero is considered an extra step down. Going
            # backwards from a starting position of zero doesn't count as a
            # step down since the zero was already passed by the previous
            # iteration. We subtract one from both the starting and ending
            # position to account for this.
            initial_iterations = (position - 1) // 100
            position -= int(line[1:])
            new_iterations = (position - 1) // 100
            password +=  initial_iterations - new_iterations
        else:
            raise ValueError(f"Invalid instruction {line}")

        position %= 100

    print(f"[Part Two] Password is {password}")

if __name__ == "__main__":
    main()
