import sys
from enum import Enum
from dataclasses import dataclass

@dataclass(frozen=True)
class Vector:
    dx: int
    dy: int

@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def add(self, vec: Vector) -> "Position":
        return Position(self.x + vec.dx, self.y + vec.dy)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

    def move(self, position: Position) -> Position:
        mapping = {
            self.RIGHT: Vector(1, 0),
            self.LEFT: Vector(-1, 0),
            self.UP: Vector(0, -1),
            self.DOWN: Vector(0, 1),
        }
        return position.add(mapping[self])

    def turn_right(self) -> "Direction":
        mapping = {
            self.RIGHT: self.DOWN,
            self.LEFT: self.UP,
            self.UP: self.RIGHT,
            self.DOWN: self.LEFT,
        }
        return mapping[self]

    @classmethod
    def from_char(cls, char: str) -> "Direction":
        match char:
            case ">":
                return cls.RIGHT
            case "<":
                return cls.LEFT
            case "^":
                return cls.UP
            case "v":
                return cls.DOWN
        raise ValueError(f"Invalid direction char '{char}'")

class Map:
    lines: list[list[str]]
    position: Position
    direction: Direction
    visited: set[Position]

    def __init__(self, lines: list[str]) -> None:
        self.lines = [list(s) for s in lines]
        self.position = self.get_initial_position()
        self.direction = Direction.from_char(self.get_char(self.position))
        self.visited = set()

    def get_char(self, position: Position) -> str:
        return self.lines[position.y][position.x]

    def is_in_bounds(self, position: Position) -> bool:
        return position.y in range(len(self.lines)) \
            and position.x in range(len(self.lines[0]))

    def get_initial_position(self) -> Position:
        guard_chars = [">", "<", "^", "v"]
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                if char in guard_chars:
                    return Position(x, y)
        raise ValueError("Couldn't find guard starting position")

    def is_obstruction(self, position: Position):
        return self.get_char(position) == "#"

    def simulate(self) -> None:
        while True:
            self.visited.add(self.position)
            position = self.direction.move(self.position)
            if not self.is_in_bounds(position):
                break

            self.lines[self.position.y][self.position.x] = "X"

            if self.is_obstruction(position):
                self.direction = self.direction.turn_right()
                continue

            self.position = position

    def count_locations(self) -> int:
        self.simulate()
        return len(self.visited)


def main():
    lines = [line.strip() for line in sys.stdin.readlines()]
    guard_map = Map(lines)
    locations = guard_map.count_locations()
    print(f"[Part one] Number of locations: {locations}")


if __name__ == "__main__":
    main()
