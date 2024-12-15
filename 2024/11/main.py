import sys

def count_stones(iteration: int, stone: int, cache: dict[tuple[int, int], int]) -> int:
    if iteration == 0:
        return 1

    result = cache.get((iteration, stone))
    if result is not None:
        return result

    result = 0
    size = len(str(stone))
    if stone == 0:
        result = count_stones(iteration - 1, 1, cache)
    elif size % 2 == 0:
        mid = int(size / 2)
        result += count_stones(iteration - 1, int(str(stone)[:mid]), cache)
        result += count_stones(iteration - 1, int(str(stone)[mid:]), cache)
    else:
        result = count_stones(iteration - 1, stone * 2024, cache)

    cache[(iteration, stone)] = result
    return result

def main():
    stones = [
        int(stone)
        for stone in sys.stdin.readline().strip().split()
    ]
    cache = {}

    count = sum(
        count_stones(25, stone, cache)
        for stone in stones
    )
    print(f"[Part one] {count} stones")

    count = sum(
        count_stones(75, stone, cache)
        for stone in stones
    )
    print(f"[Part two] {count} stones")

if __name__ == "__main__":
    main()
