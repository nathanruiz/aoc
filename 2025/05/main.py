import sys


def main():
    fresh_ranges: list[tuple[int, int]] = []
    for line in sys.stdin:
        if line.strip() == "":
            break
        start, end = line.strip().split("-")
        fresh_ranges.append((int(start), int(end)))

    ingredients: list[int] = []
    for line in sys.stdin:
        ingredients.append(int(line.strip()))

    fresh_count = 0
    for ingredient in ingredients:
        for start, end in fresh_ranges:
            if ingredient in range(start, end + 1):
                fresh_count += 1
                break

    print(f"[Part one] Number of fresh ingredients {fresh_count}")


if __name__ == "__main__":
    main()
