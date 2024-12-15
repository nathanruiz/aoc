import sys

def process_stone(stone: int) -> list[int]:
    size = len(str(stone))
    if stone == 0:
        return [1]
    elif size % 2 == 0:
        mid = int(size / 2)
        return [
            int(str(stone)[:mid]),
            int(str(stone)[mid:]),
        ]
    else:
        return [stone * 2024]

def main():
    stones = [
        int(stone)
        for stone in sys.stdin.readline().strip().split()
    ]

    for _ in range(25):
        stones = [
            new_stone
            for stone in stones
            for new_stone in process_stone(stone)
        ]

    print(f"[Part one] {len(stones)} stones")

if __name__ == "__main__":
    main()
