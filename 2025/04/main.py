from dataclasses import dataclass
import sys

@dataclass
class Bounds:
    width: int
    height: int

    def __contains__(self, location: "Location") -> bool:
        return (
            location.x >= 0 and location.y >= 0 and
            location.x < self.width and location.y < self.height
        )

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                yield Location(x, y)


@dataclass
class Location:
    x: int
    y: int

    def __add__(self, location: "Location") -> None:
        return Location(location.x + self.x, location.y + self.y)


class Grid:
    rolls: list[list[bool]]
    bounds: Bounds

    def __init__(self, lines: list[str]) -> None:
        self.rolls = [
            [cell == "@" for cell in line.strip()]
            for line in lines
        ]
        self.bounds = Bounds(
            width=len(self.rolls[0]),
            height=len(self.rolls),
        )

    def is_roll(self, location: Location) -> bool:
        if location not in self.bounds:
            return False

        return self.rolls[location.y][location.x]

    def get_accessible_rolls(self) -> list[Location]:
        locations = []
        for location in self.bounds:
            if self.is_roll(location) and self.is_accessible(location):
                locations.append(location)

        return locations

    def is_accessible(self, location: Location) -> bool:
        roll_count = 0
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                neighbor = location + Location(x, y)
                if self.is_roll(neighbor):
                    roll_count += 1

        if roll_count <= 4:
            return True

    def remove_roll(self, location: Location) -> bool:
        self.rolls[location.y][location.x] = False


def main():
    lines = sys.stdin.readlines()
    grid = Grid(lines)
    locations = grid.get_accessible_rolls()
    print(f"[Part one] Accessible rolls {len(locations)}")

    removed = 0
    while True:
        locations = grid.get_accessible_rolls()
        if len(locations) == 0:
            break

        for location in locations:
            grid.remove_roll(location)
            removed += 1

    print(f"[Part two] Removable rolls {removed}")


if __name__ == "__main__":
    main()
