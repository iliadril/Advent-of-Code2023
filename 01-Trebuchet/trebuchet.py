def get_data(filename: str) -> [str]:
    with open(filename, 'r') as f:
        return [line.rstrip() for line in f]


def get_first_digit(s: str) -> str:
    for ch in s:
        if ch.isdigit():
            return ch


def process_line(l: str) -> int:
    a = get_first_digit(l)
    b = get_first_digit(l[::-1])
    return int(a + b)


def part1() -> int:
    data = get_data("input")
    return sum(process_line(s) for s in data)


def get_number_from_line(line: str) -> int:
    chs_dict = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
    }
    nums_index = {}
    for ch in chs_dict.keys():  # check every possible number
        last_index = 0
        while True:
            i = line.find(ch, last_index)
            if i == -1:
                break
            nums_index[i] = chs_dict[ch]  # add the occurrence index
            last_index = i + 1  # save the last occurrence in order not to get stuck in a loop
    sorted_numbers = [nums_index[k] for k in sorted(nums_index.keys())]  # sort numbers by their index
    return sorted_numbers[0] * 10 + sorted_numbers[-1]  # return first and last number


def part2() -> int:
    data = get_data("input")
    return sum(get_number_from_line(line) for line in data)


if __name__ == "__main__":
    print(f"Part 1 result: {part1()}")
    print(f"Part 2 result: {part2()}")
