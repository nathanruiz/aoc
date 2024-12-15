import re
import sys
from dataclasses import dataclass


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


if __name__ == "__main__":
    main()
