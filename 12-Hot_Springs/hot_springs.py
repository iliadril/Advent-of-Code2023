import re
from dataclasses import dataclass


@dataclass
class SpringRow:
    springs: str
    group: list[int]


# ~~~~~~~~ END OF CLASSES ~~~~~~~~
def get_data(filename: str):
    with open(filename, "r") as f:
        pattern = re.compile(r"(\W+)\s([\d,]+)\s?")
        matches = pattern.findall(f.read())
        return [
            SpringRow(springs, [int(idx) for idx in group.split(",")])
            for springs, group in matches
        ]


def part1() -> int:
    spring_rows = get_data("test_input")
    pass


if __name__ == "__main__":
    print("Day 12:")
    print(f"Part 1: {part1()}")
