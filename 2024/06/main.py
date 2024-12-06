from functools import cache
import sys
from enum import Enum
from dataclasses import dataclass

class LoopError(Exception):
    pass

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
    RIGHT = ">"
    LEFT = "<"
    UP = "^"
    DOWN = "v"

    def move(self, position: Position) -> Position:
        match self:
            case self.RIGHT:
                vec = Vector(1, 0)
            case self.LEFT:
                vec = Vector(-1, 0)
            case self.UP:
                vec = Vector(0, -1)
            case self.DOWN:
                vec = Vector(0, 1)
            case v:
                raise ValueError(f"Invalid direction {v}")
        return position.add(vec)

    def turn_right(self) -> "Direction":
        match self:
            case self.RIGHT:
                return self.DOWN
            case self.LEFT:
                return self.UP
            case self.UP:
                return self.RIGHT
            case self.DOWN:
                return self.LEFT
            case v:
                raise ValueError(f"Invalid direction {v}")

    @classmethod
    def from_char(cls, char: str) -> "Direction":
        return Direction(char)

    def to_char(self) -> str:
        return self.value

class Map:
    lines: list[list[str]]
    position: Position
    direction: Direction
    visited: set[tuple[Position, Direction]]

    def __init__(
        self,
        lines: list[list[str]],
        position: Position | None=None,
        direction: Direction | None=None,
    ) -> None:
        self.lines = lines
        self.visited = set()

        if position:
            self.position = position
        else:
            self.position = self.get_initial_position()

        if direction:
            self.direction = direction
        else:
            self.direction = self.get_initial_direction()

    def get_char(self, position: Position) -> str:
        return self.lines[position.y][position.x]

    def is_in_bounds(self, position: Position) -> bool:
        return position.y in range(len(self.lines)) \
            and position.x in range(len(self.lines[0]))

    @cache
    def get_initial_position(self) -> Position:
        guard_chars = [">", "<", "^", "v"]
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                if char in guard_chars:
                    return Position(x, y)
        raise ValueError("Couldn't find guard starting position")

    def get_initial_direction(self) -> Direction:
        position = self.get_initial_position()
        return Direction.from_char(self.get_char(position))

    def is_obstruction(self, position: Position):
        return self.get_char(position) == "#"

    def simulate(self) -> None:
        while True:
            if (self.position, self.direction) in self.visited:
                raise LoopError("Loop detected in guards path")

            self.visited.add((self.position, self.direction))

            position = self.direction.move(self.position)
            if not self.is_in_bounds(position):
                break

            if self.is_obstruction(position):
                self.direction = self.direction.turn_right()
                continue

            self.position = position

    def count_positions(self) -> int:
        """
        Count the number of visited positions. This must be done after the
        simulation is complete.
        """
        if len(self.visited) == 0:
            raise ValueError("Simulation hasn't been run yet")

        return len({pos for pos, _ in self.visited})

    def count_loopers(self) -> int:
        if len(self.visited) == 0:
            raise ValueError("Simulation hasn't been run yet")

        count = 0
        obstructions = {
            direction.move(position)
            for position, direction in self.visited
        }
        obstructions.remove(self.get_initial_position())
        for position in obstructions:
            try:
                if self.is_in_bounds(position):
                    new_map = self.with_extra_obstruction(position)
                    new_map.simulate()
            except LoopError:
                count += 1

        return count

    def render(self) -> str:
        lines = [[char for char in line] for line in self.lines]
        for pos, direction in self.visited:
            lines[pos.y][pos.x] = direction.to_char()
        return "\n".join(["".join(line) for line in lines])

    def with_extra_obstruction(self, position: Position):
        lines = [[char for char in line] for line in self.lines]
        lines[position.y][position.x] = "#"
        return Map(
            lines=lines,
            position=self.get_initial_position(),
            direction=self.get_initial_direction(),
        )


def main():
    lines = [list(line.strip()) for line in sys.stdin.readlines()]
    guard_map = Map(lines)
    guard_map.simulate()
    print(f"[Part one] Number of locations: {guard_map.count_positions()}")
    print(f"[Part two] Number of loops: {guard_map.count_loopers()}")


if __name__ == "__main__":
    main()
