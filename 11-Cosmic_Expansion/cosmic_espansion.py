from itertools import combinations


Galaxy = list[list[str]]


class Point:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def distance(self, p):
        return sum(abs(val1 - val2) for val1, val2 in zip(self, p))


# ~~~~~~~~ END OF CLASSES ~~~~~~~~
def expand_vertically(galaxy: Galaxy):
    empty = [i for i, row in enumerate(galaxy) if all(char == "." for char in row)]
    for i, row in enumerate(empty):
        galaxy.insert(i + row, ["."] * len(galaxy[0]))


def expand_galaxy(galaxy: Galaxy) -> Galaxy:
    expand_vertically(galaxy)
    transposed = list(map(list, zip(*galaxy)))
    expand_vertically(transposed)
    return list(map(list, zip(*transposed)))


def get_data(filename: str):
    with open(filename, "r") as f:
        data = [[char for char in line.rstrip()] for line in f]
        data = expand_galaxy(data)
        galaxies = [
            Point(x, y) for y, row in enumerate(data) for x, char in enumerate(row) if char == "#"
        ]
        return galaxies


def part1() -> int:
    galaxies = get_data("input")
    pairs = combinations(galaxies, 2)
    return sum(a.distance(b) for a, b in pairs)


def get_part2_data(filename: str):
    with open(filename, "r") as f:
        data = [[char for char in line.rstrip()] for line in f]
        empty_rows = [i for i, row in enumerate(data) if all(char == "." for char in row)]
        empty_cols = [i for i, row in enumerate(zip(*data)) if all(char == "." for char in row)]
        galaxies = []
        for y, row in enumerate(data):
            for x, char in enumerate(row):
                if char == "#":
                    empty_rows_before = sum(y >= r for r in empty_rows)
                    empty_cols_before = sum(x >= c for c in empty_cols)
                    row_space = 1e6 * empty_rows_before - empty_rows_before if empty_rows_before else 0
                    col_space = 1e6 * empty_cols_before - empty_cols_before if empty_cols_before else 0
                    galaxies += [
                        Point(
                            x + col_space,
                            y + row_space,
                        )
                    ]
        return galaxies


def part2() -> int:
    galaxies = get_part2_data("input")
    pairs = combinations(galaxies, 2)
    return int(sum(a.distance(b) for a, b in pairs))


if __name__ == "__main__":
    print("Day 11:")
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
