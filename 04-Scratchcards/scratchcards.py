from dataclasses import dataclass
import re


@dataclass
class Scratchcard:
    winning_numbers: list[int]
    my_numbers: list[int]

    def get_winning_numbers(self):
        return set(self.winning_numbers).intersection(set(self.my_numbers))


def get_data(filename: str) -> list[Scratchcard]:
    scratchcards = []
    with open(filename, 'r') as f:
        pattern = re.compile(r":\s*([^|]+)\s*\|\s*(.+)")
        matches = pattern.findall(f.read())
        for a, b in matches:
            scratchcards += [Scratchcard([int(n) for n in a.strip().split()], [int(n) for n in b.strip().split()])]
    return scratchcards


def part1() -> int:
    scratchcards = get_data("input")
    result = 0
    for s in scratchcards:
        winning = s.get_winning_numbers()
        result += 2**(len(winning) - 1) if winning else 0
    return result


def process_scratchcards(scratchcards: list[Scratchcard], recursion_depth=0):
    total_winnings = 1
    if not scratchcards:  # end of scratchcards
        return total_winnings
    if won := len(scratchcards[0].get_winning_numbers()):
        total_winnings += won
        for i in range(won):
            total_winnings += process_scratchcards(scratchcards[i+1:], recursion_depth=recursion_depth+1)
    return total_winnings


def part2() -> int:
    scratchcards = get_data("input")
    return process_scratchcards(scratchcards) + 1


if __name__ == "__main__":
    print("Day 4:")
    print(part1())
    print(part2())
