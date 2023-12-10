import string
from collections import Counter


def get_data(filename: str):
    with open(filename, 'r') as f:
        # pad the input so that it won't get shat on while querying neighbours
        data = ['.' + line.rstrip() + '.' for line in f]  # left right pad
        data.insert(0, '.' * len(data[0]))  # top pad
        data += ['.' * len(data[0])]  # bottom pad
        return data


def check_neighbours(schematic: list[str], x_pos: int, y_pos: int,
                     num_length: int = 1, part_symbols=False) -> list[tuple[int, int]]:
    if not part_symbols:
        part_symbols = (
            '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '/', ':', ';', '<', '=', '>', '?',
            '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~')  # string.punctuation w/o the dot

    found = []
    # check top and bottom neighbours
    for x in range(x_pos - 1, x_pos + num_length + 1):
        for y in (y_pos - 1, y_pos + 1):
            if schematic[y][x] in part_symbols:
                found += [(x, y)]
    # check left
    if schematic[y_pos][x_pos - 1] in part_symbols:
        found += [(x_pos - 1, y_pos)]
    # check right
    if schematic[y_pos][x_pos + num_length] in part_symbols:
        found += [(x_pos + num_length, y_pos)]
    # not one symbol spotted :salute:
    return found


def get_parts_coordinates(schematic: list[str], part_symbols: bool | list[str] = False) -> list[
    tuple[int, int, int, tuple[int, int]]]:
    coordinates = []  # x_position, y_position, number_length, [all valid neighbours positions]
    for y, line in enumerate(schematic):
        num_length, x_pos, y_pos = 0, 0, 0  # reset every line x_pos
        for x, ch in enumerate(line):
            if ch.isdigit():  # begin checking the length of the number
                num_length += 1
                if x_pos != 0 and y_pos != 0:  # skip reassigning starting X and Y if continuation of a previous number
                    continue
                x_pos, y_pos = x, y
                continue
            elif num_length != 0:  # if !ch.isdigit() but there was some number present
                found_neighbours = check_neighbours(schematic, x_pos, y_pos, num_length, part_symbols=part_symbols)
                if found_neighbours:
                    coordinates += [(x_pos, y_pos, num_length, found_neighbours)]
                num_length, x_pos, y_pos = 0, 0, 0  # reset whenever a new digit hasn't been found
    return coordinates


def part1() -> int:
    data = get_data("input")
    result = 0

    for x_pos, y_pos, num_length, _ in get_parts_coordinates(data):
        result += int(data[y_pos][x_pos:x_pos + num_length])
    return result


def part2() -> int:
    data = get_data("input")
    result = []

    number_coordinates = {}
    symbol_coordinates = []
    for x_pos, y_pos, num_length, sym_pos in get_parts_coordinates(data, ['*']):
        number_coordinates.update({tuple((full_x, y_pos)): data[y_pos][x_pos:x_pos + num_length]
                                   for full_x in
                                   range(x_pos, x_pos + num_length)})  # all possible cords + number as value
        symbol_coordinates += sym_pos

    sym_pos_counter = Counter(symbol_coordinates)
    for sym_pos in sym_pos_counter:
        if sym_pos_counter[sym_pos] == 2:
            symbol_numbers = set()
            for num_pos in check_neighbours(data, *sym_pos, part_symbols=list(string.digits)):
                symbol_numbers.add(number_coordinates[num_pos])
            a, b = [int(n) for n in symbol_numbers]
            result += [a * b]
    return sum(result)


if __name__ == "__main__":
    print("Day 3:")
    print(part1())
    print(part2())
