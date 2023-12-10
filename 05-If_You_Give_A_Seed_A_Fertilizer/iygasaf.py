import re
from dataclasses import dataclass


@dataclass
class CategoryValue:
    destination_start: int
    source_start: int
    range_length: int

    def get_destination(self, source: int):  # return destination -1 when not found
        # get the difference between lower and upper bound of source values
        range_increment = self.range_length - 1
        upper_bound = self.source_start + range_increment  # highest valid source number
        diff = upper_bound - source
        if 0 <= diff <= range_increment:
            return self.destination_start + range_increment - diff
        return -1

    def split_on_extremes(self, source_range: range) -> list[range]:
        destination_ranges = []
        my_range = range(self.source_start, self.source_start + self.range_length)
        # check whether [M]my_range or [S]source_range [L]lower or [U]upper bounds are inside
        m_l = my_range[0] in source_range
        m_u = my_range[-1] in source_range
        s_l = source_range[0] in my_range
        s_u = source_range[-1] in my_range
        if not (m_l or m_u or s_l or s_u):
            return []  # add full range as output
        else:  # add intersection, calculate destination
            offset = (
                max(my_range[0], source_range[0]) - min(my_range[0], source_range[0])
                if not m_l
                else 0
            )
            diff = min(my_range[-1], source_range[-1]) + 1 - max(my_range[0], source_range[0])
            destination_ranges += [
                range(self.destination_start + offset, self.destination_start + diff + offset)
            ]
            if m_l and not s_l:  # add lower difference
                destination_ranges += [range(source_range[0], my_range[0])]
            if m_u and not s_u:  # add upper difference
                destination_ranges += [range(my_range[-1] + 1, source_range[-1] + 1)]
            return destination_ranges


@dataclass
class CategoryMap:
    name: str
    values: list[CategoryValue]

    def get_destination_value(self, source: int) -> int:
        destination = source
        for cat_val in self.values:
            found = cat_val.get_destination(source)
            if found != -1:
                destination = found
                break
        return destination

    def get_extreme_ranges(self, source_range: list[range]) -> list[range]:
        total_extremes = []
        for c_val in self.values:
            local_extremes = []
            extremes = source_range[:]
            while extremes:
                extreme = extremes.pop(0)
                local_extremes += c_val.split_on_extremes(extreme)
            total_extremes += local_extremes
        return total_extremes if total_extremes else source_range


# ~~~~~~~~ END OF CLASSES ~~~~~~~~


def get_data(filename: str) -> tuple[list[int], list[CategoryMap]]:
    with open(filename, "r") as f:
        seeds = [int(num) for num in f.readline().rstrip().split(":")[1].split()]
        map_pattern = re.compile(r"(.*)\smap:\s*([\s\d]+)")  # get numbers from each map
        matches = map_pattern.findall(f.read())
        cat_maps: list[CategoryMap] = []
        for map_name, values in matches:
            cat_maps += [
                CategoryMap(
                    map_name,
                    [
                        CategoryValue(*value)
                        for value in [
                            [int(num) for num in line.split()]
                            for line in values.rstrip().split("\n")
                        ]
                    ],
                )
            ]
        return seeds, cat_maps


def get_lowest_location_naive(seeds: list[int], category_maps: list[CategoryMap]) -> int:
    result = []
    for _, seed in enumerate(seeds):
        for category_map in category_maps:
            seed = category_map.get_destination_value(seed)
        result += [seed]
    return min(result)


def part1() -> int:
    seeds, category_maps = get_data("input")
    return get_lowest_location_naive(seeds, category_maps)


# ~~~~~~~~ PART 2 ~~~~~~~~


def get_seed_ranges(seeds: list[int]) -> list[range]:
    i_seeds = iter(seeds)
    return [range(start, start + length) for start, length in zip(i_seeds, i_seeds)]


def get_lowest_location(seed_ranges: list[range], category_maps: list[CategoryMap]) -> int:
    total_result = []
    for seed_range in seed_ranges:
        result = [seed_range]
        for category_map in category_maps:
            result = category_map.get_extreme_ranges(result)
        total_result += result

    return min([value_range[0] for value_range in total_result])


def part2() -> int:
    raw_seeds, category_maps = get_data("test_input")
    return get_lowest_location(get_seed_ranges(raw_seeds), category_maps)


if __name__ == "__main__":
    print("Day 5:")
    print(part1())
    print(part2())
