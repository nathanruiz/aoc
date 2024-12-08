from dataclasses import dataclass
from collections import defaultdict
from itertools import count, permutations
import sys

@dataclass(frozen=True)
class Vector:
    dx: int
    dy: int

    def __mul__(self, value: int) -> "Vector":
        return Vector(self.dx * value, self.dy * value)

@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, vec: Vector) -> "Position":
        return Position(self.x + vec.dx, self.y + vec.dy)

    def __sub__(self, pos: "Position") -> Vector:
        return Vector(self.x - pos.x, self.y - pos.y)

class TowerMap:
    grid: list[str]

    def __init__(self, grid: list[str]):
        self.grid = grid
        self.bounds = (len(grid[0]), len(grid))

    def is_in_bounds(self, position: Position) -> bool:
        mx, my = self.bounds
        return position.x >= 0 and position.x < mx \
            and position.y >= 0 and position.y < my

    def get_towers(self) -> dict[str, Position]:
        results = defaultdict(list)
        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if char.isalnum():
                    results[char].append(Position(x, y))
        return results

    def get_antinodes(self) -> set[Position]:
        antinodes = list()
        for char, positions in self.get_towers().items():
            for a, b in permutations(positions, 2):
                antinodes.append(a + (a - b))
                antinodes.append(b + (b - a))
        return {
            antinode
            for antinode in antinodes
            if self.is_in_bounds(antinode)
        }

    def get_antinodes_with_resonant_harmonics(self) -> set[Position]:
        antinodes = set()
        for char, positions in self.get_towers().items():
            for a, b in permutations(positions, 2):
                for delta, start in [(a - b, a), (b - a, b)]:
                    for i in count():
                        pos = start + (delta * i)
                        if not self.is_in_bounds(pos):
                            break
                        antinodes.add(pos)
        return antinodes

def main():
    grid = [line.strip() for line in sys.stdin.readlines()]
    tower_map = TowerMap(grid)
    antinodes = tower_map.get_antinodes()
    print(f"[Part one] Number of antinodes {len(antinodes)}")

    antinodes = tower_map.get_antinodes_with_resonant_harmonics()
    print(f"[Part two] Number of antinodes {len(antinodes)}")


if __name__ == "__main__":
    main()
