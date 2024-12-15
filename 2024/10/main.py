import sys
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def add(self, x: int, y: int) -> "Point":
        return Point(self.x + x, self.y + y)

class Grid:
    lines: list[list[int]]

    def __init__(self, lines: list[str]) -> None:
        self.lines = [
            [int(cell) for cell in line]
            for line in lines
        ]

    def get_trailheads(self) -> list[Point]:
        points = []
        for y, row in enumerate(self.lines):
            for x, cell in enumerate(row):
                if cell == 0:
                    points.append(Point(x, y))
        return points

    def get_height(self, point: Point) -> int:
        return self.lines[point.y][point.x]

    def get_neighbors(self, point: Point) -> list[Point]:
        return [
            point
            for point in [
                point.add(1, 0),
                point.add(0, 1),
                point.add(-1, 0),
                point.add(0, -1),
            ]
            if point.y in range(len(self.lines))
            and point.x in range(len(self.lines[0]))
        ]

    def get_sumits(self, point: Point) -> set[Point]:
        """
        Get all the possible sumit locations reachable from this point.
        """
        height = self.get_height(point)
        if height == 9:
            return {point}

        sumits = set()
        for neighbor in self.get_neighbors(point):
            if self.get_height(neighbor) == height + 1:
                sumits.update(self.get_sumits(neighbor))

        return sumits

    def get_sumit_paths(self, path: Sequence[Point]) -> set[Sequence[Point]]:
        """
        Get all the possible sumit locations reachable from this point.
        """
        head = path[-1]
        height = self.get_height(head)
        if height == 9:
            return {path}

        paths = set()
        for neighbor in self.get_neighbors(head):
            if self.get_height(neighbor) == height + 1:
                paths.update(self.get_sumit_paths((*path, neighbor)))

        return paths

def main():
    grid = Grid([line.strip() for line in sys.stdin.readlines()])

    score = 0
    trailheads = grid.get_trailheads()
    for trailhead in trailheads:
        score += len(grid.get_sumits(trailhead))

    print("[Part one] trailhead scores:", score)

    score = 0
    for trailhead in trailheads:
        score += len(grid.get_sumit_paths((trailhead,)))

    print("[Part two] trailhead scores:", score)


if __name__ == "__main__":
    main()
