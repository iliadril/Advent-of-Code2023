from typing import ClassVar
from collections import Counter
from dataclasses import dataclass
from functools import total_ordering


@dataclass
@total_ordering
class Hand:
    cards: list[str]
    bid: int

    card_strength: ClassVar[str] = "AKQT98765432J"

    def hand_strength(self) -> int:
        # Five of a kind -> Four of a kind -> Full house -> Three of a kind -> Two pair -> One pair -> High card
        optimal_hand = self.get_optimal_hand()
        assert len(self.cards) == 5, "Invalid hand length."
        counter = Counter(optimal_hand)
        # Five of a kind e.g. AA8AA
        if any(count == 5 for count in counter.values()):
            return 7
        # Four of a kind e.g. AA8AA
        elif any(count == 4 for count in counter.values()):
            return 6
        # Full house e.g. 23332
        elif any(c == 3 for c in counter.values()) and any(c == 2 for c in counter.values()):
            return 5
        # Three of a kind e.g. TTT98
        elif any(count == 3 for count in counter.values()):
            return 4
        # Two pair e.g. 23432
        elif sum(1 for count in counter.values() if count == 2) == 2:
            return 3
        # One pair e.g. A23A4
        elif any(count == 2 for count in counter.values()):
            return 2
        else:
            return 1

    def get_optimal_hand(self) -> list[str]:
        jokerless = [c for c in self.cards if c != "J"]
        if not jokerless:
            return ["A"] * 5
        most_common = Counter(jokerless).most_common(1)[0][0]
        return [c if c != "J" else most_common for c in self.cards]

    def __eq__(self, other):
        if not isinstance(other, Hand):
            raise NotImplemented
        return self.cards == other.cards

    def __lt__(self, other):
        if not isinstance(other, Hand):
            raise NotImplemented
        if self.hand_strength() < other.hand_strength():
            return True
        elif self.hand_strength() == other.hand_strength():
            for card, other_card in zip(self.cards, other.cards):
                if self.card_strength.index(card) == self.card_strength.index(other_card):
                    continue
                return self.card_strength.index(card) > self.card_strength.index(other_card)
        return False


# ~~~~~~~~ END OF CLASSES ~~~~~~~~


def get_data(filename: str) -> list[Hand]:
    with open(filename, "r") as f:
        return [
            Hand(list(cards), int(bid)) for line in f for (cards, bid) in [line.rstrip().split()]
        ]


def part2() -> int:
    cards = get_data("input")
    sorted_cards = sorted(cards)
    # print(*list([(hand, hand.hand_strength()) for hand in sorted_cards]), sep="\n")
    return sum(i * hand.bid for i, hand in enumerate(sorted_cards, start=1))


if __name__ == "__main__":
    print("Day 7:")
    print(part2())
