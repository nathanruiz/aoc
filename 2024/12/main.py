import re
import sys
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def add(self, x: int, y: int) -> "Point":
        return Point(self.x + x, self.y + y)

    def neighbors(self) -> list["Point"]:
        return [
            self.add(0, 1),
            self.add(1, 0),
            self.add(0, -1),
            self.add(-1, 0),
        ]

    def get_line_between(self, point: "Point") -> Direction:
        if point.y == self.y:
            if point.x == self.x + 1:
                return Direction.DOWN
            elif point.x == self.x - 1:
                return Direction.UP
        elif point.x == self.x:
            if point.y == self.y + 1:
                return Direction.RIGHT
            elif point.y == self.y - 1:
                return Direction.LEFT
        raise ValueError("Invalid direction")

@dataclass
class Region:
    points: set[Point]

    def get_area(self) -> int:
        return len(self.points)

    def get_perimeter(self) -> int:
        perimeter = 0
        for point in self.points:
            for neighbor in point.neighbors():
                if neighbor not in self.points:
                    perimeter += 1
        return perimeter

    def get_sides(self) -> int:
        lines = []
        for point in self.points:
            for neighbor in point.neighbors():
                if neighbor not in self.points:
                    lines.append((point, point.get_line_between(neighbor)))

        result = []
        while lines:
            line = lines.pop()
            result.append(line)
            open_set = {line}
            closed_set = set()
            while open_set:
                point, direction = open_set.pop()
                for neighbor in point.neighbors():
                    key = (neighbor, direction)
                    if key in closed_set:
                        continue

                    if key in lines:
                        lines.remove(key)
                        open_set.add(key)

        return len(result)


class Garden:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def get_plant_type(self, point: Point) -> str | None:
        if point.y in range(len(self.lines)):
            if point.x in range(len(self.lines[0])):
                return self.lines[point.y][point.x]
        return None

    def get_regions(self) -> list[Region]:
        visited = set()
        regions = []
        for y, row in enumerate(self.lines):
            for x, cell in enumerate(row):
                point = Point(x, y)
                if point in visited:
                    continue

                region = self.get_region(point)
                visited = visited | region.points
                regions.append(region)
        return regions

    def get_region(self, point: Point) -> Region:
        open_set = {point}
        plant_type = self.get_plant_type(point)
        closed_set = set()
        while open_set:
            point = open_set.pop()
            closed_set.add(point)
            for neighbor in point.neighbors():
                if self.get_plant_type(neighbor) != plant_type:
                    continue

                if neighbor in closed_set:
                    continue

                open_set.add(neighbor)
        return Region(closed_set)

def main():
    garden = Garden([line.strip() for line in sys.stdin.readlines()])
    regions = garden.get_regions()

    price = sum(
        region.get_area() * region.get_perimeter()
        for region in regions
    )
    print("[Part one] Total price:", price)

    price = sum(
        region.get_area() * region.get_sides()
        for region in regions
    )
    print("[Part two] Total price:", price)


if __name__ == "__main__":
    main()
