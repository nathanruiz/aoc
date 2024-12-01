import sys
from collections import defaultdict

def main():
    # Read all lines from stdin
    lines = [
        line.strip().split()
        for line in sys.stdin.readlines()
    ]

    # Split the lines into columns
    left_column, right_column = zip(*lines)

    # Convert the input text to sorted numbers
    left_column = sorted(int(n) for n in left_column)
    right_column = sorted(int(n) for n in right_column)

    # Loop through the sorted columns, and sum up the differences.
    diff = sum(abs(left - right) for left, right in zip(left_column, right_column))

    print(f"[Part one] Total difference: {diff}")

    # Calculate the occurance count for each value in the right column.
    occurances = defaultdict(lambda: 0)
    for n in right_column:
        occurances[n] += 1

    # Calculate the similarity cost
    similarity = sum(n * occurances[n] for n in left_column)

    print(f"[Part two] Similarity score: {similarity}")


if __name__ == "__main__":
    main()
