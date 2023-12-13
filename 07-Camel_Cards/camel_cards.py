from dataclasses import dataclass


@dataclass
class Hand:
    cards: list[str]
    bid: int


# ~~~~~~~~ END OF CLASSES ~~~~~~~~


def get_data(filename: str) -> list[Hand]:
    with open(filename, "r") as f:
        return [
            Hand(cards.split(), int(bid)) for line in f for (cards, bid) in [line.rstrip().split()]
        ]


def part1() -> int:
    return get_data("test_input")


if __name__ == "__main__":
    print("Day 7:")
    print(part1())
