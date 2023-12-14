def get_data(filename: str) -> list[list[int]]:
    with open(filename, "r") as f:
        return [[int(num) for num in line.rstrip().split()] for line in f]


def extrapolate(history: list[int]):
    result = []
    for (a, b) in zip(history, history[1:]):
        result += [b - a]
    return result


def part1() -> int:
    histories = get_data("input")
    result = []
    for history in histories:
        extrapolated: list[list[int]] = [history]
        i = 0
        while not all(num == 0 for num in extrapolated[-1]):
            extrapolated += [extrapolate(extrapolated[i])]
            i += 1
        for _ in range(i):
            i -= 1
            extrapolated[i] += [extrapolated[i][-1] + extrapolated[i + 1][-1]]
        result += [extrapolated[0][-1]]

    return sum(result)


if __name__ == "__main__":
    print("Day 9:")
    print(f"Part 1: {part1()}")
