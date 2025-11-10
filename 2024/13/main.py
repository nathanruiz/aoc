import math
import sys
import re
from dataclasses import dataclass
import dataclasses


@dataclass(frozen=True)
class Vector:
    dx: int
    dy: int

    def __mul__(self, value: int) -> "Vector":
        return Vector(self.dx * value, self.dy * value)

    def inverse(self) -> "Vector":
        return Vector(-self.dx, -self.dy)

    def steps(self, v: "Vector") -> int:
        return math.ceil(max(
            v.dx / self.dx,
            v.dy / self.dy,
        ))

@dataclass(frozen=True)
class Position:
    x: int
    y: int

    @classmethod
    def origin(cls) -> "Position":
        return Position(0, 0)

    def __add__(self, vec: Vector) -> "Position":
        return Position(self.x + vec.dx, self.y + vec.dy)

    def __sub__(self, pos: "Position") -> Vector:
        return Vector(self.x - pos.x, self.y - pos.y)

@dataclass(frozen=True)
class Machine:
    button_a: Vector
    button_b: Vector
    target: Position

    def position_after(self, a_steps: int, b_steps: int) -> Position:
        return Position.origin() + (self.button_a * a_steps) + (self.button_b * b_steps)

    def calculate_steps(self) -> tuple[int, int] | None:
        a_steps = 0
        b_steps = self.button_b.steps(self.target - Position.origin())

        while True:
            position = self.position_after(a_steps, b_steps)

            if position == self.target:
                return (a_steps, b_steps)

            # If either X or Y positions are less than the target, add button
            # A's vector.
            while position.x < self.target.x or position.y < self.target.y:
                steps = self.button_a.steps(self.target - position)
                a_steps += steps
                position += self.button_a * steps

            # If either X or Y positions are larger than the target, remove
            # button B's vector.
            while position.x > self.target.x or position.y > self.target.y:
                steps = self.button_b.inverse().steps(self.target - position)
                b_steps -= steps
                position += self.button_b.inverse() * steps

                if b_steps < 0:
                    return None


    def calculate_cost(self) -> int | None:
        steps = self.calculate_steps()
        if steps is None:
            return None

        return (steps[0] * 3) + steps[1]


BUTTON_A_PATTERN = re.compile(r"Button A: X\+([0-9]+), Y\+([0-9]+)")
BUTTON_B_PATTERN = re.compile(r"Button B: X\+([0-9]+), Y\+([0-9]+)")
TARGET_PATTERN = re.compile(r"Prize: X=([0-9]+), Y=([0-9]+)")

def parse_coords(pattern, value) -> (int, int):
    return [int(v) for v in re.match(pattern, value).groups()]

def main():
    records = sys.stdin.read().split("\n\n")
    part_1_total_cost = 0
    part_2_total_cost = 0

    for record in records:
        lines = record.split("\n")
        button_a = parse_coords(BUTTON_A_PATTERN, lines[0])
        button_b = parse_coords(BUTTON_B_PATTERN, lines[1])
        target = parse_coords(TARGET_PATTERN, lines[2])

        # Calculate the cost for part 1's machine.
        machine = Machine(
            button_a=Vector(*button_a),
            button_b=Vector(*button_b),
            target=Position(*target),
        )

        cost = machine.calculate_cost()
        if cost is not None:
            part_1_total_cost += cost


        # Calculate the cost for part 2's machine.
        machine = dataclasses.replace(
            machine,
            target=machine.target + Vector(10000000000000, 10000000000000),
        )
        cost = machine.calculate_cost()
        if cost is not None:
            part_2_total_cost += cost

    print(f"[Part 1] Total cost {part_1_total_cost}")
    print(f"[Part 2] Total cost {part_2_total_cost}")

if __name__ == "__main__":
    main()
