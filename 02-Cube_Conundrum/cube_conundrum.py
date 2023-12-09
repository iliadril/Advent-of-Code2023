def get_data(filename: str) -> dict:
    with open(filename, 'r') as f:
        data = {}
        for i, line in enumerate(f, start=1):
            processed_line = line[line.find(':') + 1:].split(';')
            # data[i] = [subset.strip().split(', ') for subset in processed_line]
            data[i] = [{colour.split()[1][0]: int(colour.split()[0])} for subset in processed_line
                       for colour in subset.strip().split(', ')]
        return data


def check_if_possible(game: list[dict]) -> bool:
    max_values = {'r': 12, 'g': 13, 'b': 14}
    for res in game:
        for key, val in res.items():
            if val > max_values[key]:
                return False
    return True


def part1() -> int:
    data = get_data("input")
    result = 0
    for index, game in data.items():
        if check_if_possible(game):
            result += index
    return result


def get_power(game: list[dict]) -> int:
    min_colours = {key: max(d.get(key, float('-inf')) for d in game) for key in set().union(*game)}
    res = 1
    for colours in min_colours.values():
        res *= colours
    return res


def part2() -> int:
    data = get_data("input")
    return sum(get_power(p) for p in data.values())


if __name__ == "__main__":
    print(part1())
    print(part2())
