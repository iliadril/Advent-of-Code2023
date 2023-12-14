import re
from dataclasses import dataclass

NodeDict = dict[str, tuple[str, str]]

# ~~~~~~~~ END OF CLASSES ~~~~~~~~
def get_data(filename: str) -> tuple[str, NodeDict, str]:
    with open(filename, "r") as f:
        instructions: str = f.readline().rstrip()
        pattern = re.compile(r"(\w{3}).{4}(\w{3}), (\w{3})\)\s?")
        matches = pattern.findall(f.read())
        start_node, _, _ = matches[0]
        nodes: NodeDict = {name: (left, right) for name, left, right in matches}
        return instructions, nodes, start_node

def traverse(path: str, nodes: NodeDict, start_node: str) -> int:
    i = 0
    current_node = "AAA"
    while current_node != "ZZZ":
        if path[i % len(path)] == "L":
            current_node = nodes[current_node][0]
        elif path[i % len(path)] == "R":
            current_node = nodes[current_node][1]
        i += 1
    return i


def part1() -> int:
    path, nodes, start_node = get_data("test_recursion_input")
    return traverse(path, nodes, start_node)


if __name__ == "__main__":
    print("Day 8:")
    print(part1())
