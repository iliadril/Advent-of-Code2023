import re
from dataclasses import dataclass


class Node:
    def __init__(self, name: str, left_target: str, right_target: str):
        self.name: str = name
        self.left: Node = None
        self.right: Node = None
        self.left_target: str = left_target
        self.right_target: str = right_target

    def construct(self, nodes: list, trace=None) -> list:
        if trace is None:
            trace = []
        trace += [self]
        if self.name == self.left_target and self.name == self.right_target:
            self.left = self
            self.right = self
            return nodes
        for other_node in nodes:
            if other_node.name == self.left_target:
                if other_node.left is None and other_node.right is None and other_node not in trace:
                    nodes = other_node.construct(nodes, trace)
                self.left = other_node
            if other_node.name == self.right_target:
                if other_node.left is None and other_node.right is None and other_node not in trace:
                    nodes = other_node.construct(nodes, trace)
                self.right = other_node
        return nodes

    def dfs(self, other_name: str, found=None):
        if found is None:
            found = self
        if self.name == other_name:
            return self
        if self.name == self.left_target and self.name == self.right_target:  # loop
            return found

        found = self.left.dfs(other_name, found)
        found = self.right.dfs(other_name, found)
        return found

    def traverse_path(self, path: str) -> int:
        i = 0
        current_node = self
        while current_node.name != "ZZZ":
            if path[i % len(path)] == "L":
                current_node = current_node.left
            elif path[i % len(path)] == "R":
                current_node = current_node.right
            i += 1
            if i % 1000000 == 0:
                print(f"{i:,}")

        return i

    def __repr__(self):
        return f'Node(\'{self.name}\', {self.left_target}, {self.right_target})'


# ~~~~~~~~ END OF CLASSES ~~~~~~~~
def get_data(filename: str) -> tuple[str, Node]:
    with open(filename, "r") as f:
        instructions: str = f.readline().rstrip()
        pattern = re.compile(r"(\w{3}).{4}(\w{3}), (\w{3})\)\s?")
        matches = pattern.findall(f.read())
        nodes: list[Node] = [Node(name, left, right) for name, left, right in matches]
        root_node = nodes[0]
        return instructions, root_node.construct(nodes)[0]


def part1() -> int:
    path, root_node = get_data("test_input")
    return root_node.traverse_path(path)


if __name__ == "__main__":
    print("Day 8:")
    print(part1())
