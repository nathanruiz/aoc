import sys


class BatteryBank:
    bank: list[int]

    def __init__(self, line: str) -> None:
        self.bank = [int(char) for char in line]

    def get_largest_joltage(self, battery_count: int) -> int:
        joltage = 0
        start = 0
        for i in range(battery_count):
            # For the next digit, we need to skip over any digits we have
            # already passed over previously, and leave at least enough
            # elements at the end to find the remaining a
            end = len(self.bank) - battery_count + 1 + i
            bank = self.bank[start:end]
            position = self.find_max_value_position(bank)

            joltage = (joltage * 10) + bank[position]
            start += position + 1

        return joltage

    def find_max_value_position(self, bank: list[int]) -> int:
        max_jolts = 0
        position = 0
        for i, jolts in enumerate(bank):
            if jolts > max_jolts:
                max_jolts = jolts
                position = i
        return position



def main():
    part1_total = 0
    part2_total = 0
    for line in sys.stdin:
        line = line.strip()
        bank = BatteryBank(line)
        part1_total += bank.get_largest_joltage(2)
        part2_total += bank.get_largest_joltage(12)
    print(f"[Part one] Battery bank joltage sum {part1_total}")
    print(f"[Part two] Battery bank joltage sum {part2_total}")

if __name__ == "__main__":
    main()
