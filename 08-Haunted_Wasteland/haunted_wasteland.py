import re
import math

NodeDict = dict[str, tuple[str, str]]


# ~~~~~~~~ END OF CLASSES ~~~~~~~~
def get_data(filename: str) -> tuple[str, NodeDict]:
    with open(filename, "r") as f:
        instructions: str = f.readline().rstrip()
        pattern = re.compile(r"(\w{3}).{4}(\w{3}), (\w{3})\)\s?")
        matches = pattern.findall(f.read())
        nodes: NodeDict = {name: (left, right) for name, left, right in matches}
        return instructions, nodes


def traverse(path: str, nodes: NodeDict, start_node: str) -> int:
    i = 0
    current_node = start_node
    while current_node != "ZZZ":
        if path[i % len(path)] == "L":
            current_node = nodes[current_node][0]
        elif path[i % len(path)] == "R":
            current_node = nodes[current_node][1]
        i += 1
    return i


def ghost_traverse(path: str, nodes_dict: NodeDict) -> int:
    acc = 0
    current_nodes: list[str] = [key for key in nodes_dict.keys() if key.endswith("A")]
    steps = [0 for _ in current_nodes]  # store when "**Z" was found in each node
    while not all(node.endswith("Z") for node in current_nodes):
        for i, node in enumerate(current_nodes):
            if not node.endswith("Z"):  # only iterate further if needed
                if path[acc % len(path)] == "L":
                    current_nodes[i] = nodes_dict[node][0]
                elif path[acc % len(path)] == "R":
                    current_nodes[i] = nodes_dict[node][1]
                steps[i] = acc + 1  # +1 since we skip the last one
        acc += 1
    return math.lcm(*steps)  # get number of iteration for all cycles to end on "**Z"


def part1() -> int:
    path, nodes = get_data("input")
    return traverse(path, nodes, "AAA")


def part2() -> int:
    path, nodes = get_data("input")
    return ghost_traverse(path, nodes)


if __name__ == "__main__":
    print("Day 8:")
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
