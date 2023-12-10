from dataclasses import dataclass
import re


@dataclass
class CategoryValue:
    destination_range: int
    source_range: int
    range_length: int

    def get_destination(self, source: int):  # return destination -1 when not found
        range_increment = self.range_length - 1  # difference between lower and upper bound of source values
        upper_bound = self.source_range + range_increment  # highest valid source number
        diff = upper_bound - source
        if 0 <= diff <= range_increment:
            return self.destination_range + range_increment - diff
        return -1


@dataclass
class CategoryMap:
    name: str
    values: list[CategoryValue]

    def get_destination_value(self, source: int):
        destination = source
        for cat_val in self.values:
            found = cat_val.get_destination(source)
            if found != -1:
                destination = found
                break
        return destination


def get_data(filename: str) -> tuple[list[int], list[CategoryMap]]:
    with open(filename, 'r') as f:
        seeds = [int(num) for num in f.readline().rstrip().split(':')[1].split()]
        map_pattern = re.compile(r"(.*)\smap:\s*([\s\d]+)")  # get numbers from each map
        matches = map_pattern.findall(f.read())
        category_maps = []
        for map_name, values in matches:
            category_maps += [CategoryMap(map_name,
                                          [CategoryValue(*value) for value in [[int(num) for num in line.split()]
                                                                               for line in values.rstrip().split('\n')]])]
        return seeds, category_maps


def part1() -> int:
    seeds, category_maps = get_data("input")
    result = []
    for seed in seeds:
        for category_map in category_maps:
            seed = category_map.get_destination_value(seed)
        result += [seed]
    return min(result)


if __name__ == "__main__":
    print("Day 5:")
    print(part1())