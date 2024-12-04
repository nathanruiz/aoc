from typing import List, Tuple
import sys

class Grid:
    grid: List[str]

    def __init__(self, grid: List[str]) -> None:
        self.grid = grid
        self.x_bounds = range(len(grid))
        self.y_bounds = range(len(grid[0]))

    def count_xmas(self):
        """
        Count the number of times the word XMAS appears in the cross word, in
        any direction.
        """
        # Define the possible directions of the word, as a vector on the x and y
        # axises.
        directions = [
            (dx, dy)
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
        ]

        count = 0
        for x in self.x_bounds:
            for y in self.y_bounds:
                for direction in directions:
                    if self.is_xmas((x, y), direction):
                        count += 1
        return count

    def count_x_mas(self):
        """
        Count the number of times an "X-MAS" (two diagonal MAS that form an X)
        appears in the cross word. For example:

            M.S
            .A.
            M.S
        """
        count = 0
        for x in self.x_bounds:
            for y in self.y_bounds:
                if self.is_x_mas((x, y)):
                    count += 1
        return count

    def is_in_bounds(self, x: int, y: int) -> bool:
        """
        Check if a position is still within the bounds of the grid.
        """
        return x in self.x_bounds and y in self.y_bounds

    def is_xmas(self, position: Tuple[int, int], direction: Tuple[int, int]) -> bool:
        """
        Figure out if the word XMAS start on our currect character going in a
        specific direction.
        """
        return self.is_word(position, direction, "XMAS")

    def is_x_mas(self, position: Tuple[int, int]) -> bool:
        """
        Figure out if you are current in the center of an X-MAS.
        """
        word = "MAS"
        x, y = position
        first = self.is_word((x, y), (1, 1), word) \
            or self.is_word((x, y), (1, 1), reversed(word))

        second = self.is_word((x, y + 2), (1, -1), word) \
            or self.is_word((x, y + 2), (1, -1), reversed(word))

        return first and second


    def is_word(self, position: Tuple[int, int], direction: Tuple[int, int], word: str) -> bool:
        """
        Figure out if a word starts on our currect character going in a
        specific direction.
        """
        dx, dy = direction
        x, y = position
        for letter in word:
            if not self.is_in_bounds(x, y):
                return False

            if self.grid[x][y] != letter:
                return False

            x += dx
            y += dy

        return True



def main():
    grid = Grid([line.strip() for line in sys.stdin.readlines()])

    print(f"[Part one] XMAS count: {grid.count_xmas()}")
    print(f"[Part two] XMAS count: {grid.count_x_mas()}")


if __name__ == "__main__":
    main()
