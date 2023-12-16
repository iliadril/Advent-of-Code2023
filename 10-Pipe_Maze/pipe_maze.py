class Point:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

    def __add__(self, other):
        if not isinstance(other, Point):
            raise NotImplemented
        self.x += other.x
        self.y += other.y
        return Point(self.x, self.y)

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            raise NotImplemented
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        if not isinstance(other, Point):
            raise NotImplemented
        return self.x != other.x or self.y != other.y

    @staticmethod
    def from_char(char: str) -> list['Point']:
        assert len(char) == 1, "Input only 1 char"
        pipe_dict = {
            "S": [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)],
            ".": [],
            "F": [Point(0, 1), Point(1, 0)],
            "7": [Point(0, 1), Point(-1, 0)],
            "J": [Point(0, -1), Point(-1, 0)],
            "L": [Point(0, -1), Point(1, 0)],
            "-": [Point(-1, 0), Point(1, 0)],
            "|": [Point(0, -1), Point(0, 1)],
        }
        return pipe_dict[char]


class MazeChar:
    def __init__(self, char: str, mask: str = "I"):
        self.char = char
        self.mask = mask

    def __repr__(self):
        return f"MazeChar(char={self.char}, mask={self.mask})"


class MazeTile(MazeChar):
    def __init__(self, position: Point, char: str):
        super().__init__(char)
        self.position = position
        self.leads_to = [output + position for output in Point.from_char(char)]

    def is_valid_route(self, target: Point, maze: list[list['MazeTile']]):
        return target in self.leads_to and self.position in maze[target.y][target.x].leads_to

    def loop(self, maze: list[list['MazeTile']]) -> list[Point]:
        current_pipe = self
        route = [self.position]
        while bool(len(route) == 1) != bool(current_pipe != self):
            possibilities = [[x, y] for x, y in current_pipe.leads_to
                             if current_pipe.is_valid_route(Point(x, y), maze)
                             and Point(x, y) not in route]
            if not possibilities:
                # route += [self.position]
                break
            for x, y in possibilities:
                current_pipe = maze[y][x]
                current_pipe.mask = "P"
                route += [Point(x, y)]
                break
        return route

    def to_maze_char(self):
        return MazeChar(self.char, self.mask)

    def __repr__(self):
        return f"MazeTile(position={self.position}, leads_to={self.leads_to})"


def get_data(filename: str) -> list[list[MazeTile]]:
    with open(filename, "r") as f:
        data = ['.' + line.rstrip() + '.' for line in f]  # left right pad
        data.insert(0, '.' * len(data[0]))  # top pad
        data += ['.' * len(data[0])]  # bottom pad
        return [[MazeTile(Point(x, y), char) for x, char in enumerate(line)]
                for y, line in enumerate(data)]


def part1() -> int:
    maze = get_data("input")
    x, y = [(x, y) for y, line in enumerate(maze) for x, pipe in enumerate(line) if len(pipe.leads_to) == 4][0]
    return len(maze[y][x].loop(maze)) // 2


def mask_outside(maze: list[list[MazeChar]]) -> list[list[MazeChar]]:
    for y, line in enumerate(maze):
        for x, pipe in enumerate(line):
            if pipe.mask != "P":
                if y == 0 or y == len(maze) - 1 or x == 0 or x == len(maze[0]) - 1:
                    pipe.mask = "O"
                    continue
                if any(maze[j][i].mask == "O" for i, j in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]):
                    pipe.mask = "O"
    return maze


def flood_fill(maze: list[list[MazeChar]], x: int = 1, y: int = 1):
    nodes = [(maze[y][x], Point(x, y))]
    while nodes:
        current_node, point = nodes.pop(0)
        x, y = point
        if current_node.mask in ["I", "L"]:
            current_node.mask = "O"
            nodes += [(maze[y][x - 1], Point(x - 1, y))]
            nodes += [(maze[y][x + 1], Point(x + 1, y))]
            nodes += [(maze[y - 1][x], Point(x, y - 1))]
            nodes += [(maze[y + 1][x], Point(x, y + 1))]
    return


def horizontal_expand(maze: list[list[MazeChar]]) -> list[list[MazeChar]]:
    for row in maze:
        started = False
        for x in range(len(row)):  # for some reason enumerate(row) doesnt work lol
            if row[x * 2].char in ["S", "J", "-", "7", "F", "L"]:
                if row[x * 2 - 1].char in ["7", "J"]:
                    row.insert(x * 2, MazeChar("-", "P") if not started else MazeChar(".", "L"))
                else:
                    row.insert(x * 2, MazeChar("-", "P") if started else MazeChar(".", "L"))
                started = True
            else:
                row.insert(x * 2, MazeChar(".", "L"))
                started = False
    return maze


def vertical_expand(maze: list[list[MazeChar]]) -> list[list[MazeChar]]:
    maze = list(map(list, zip(*maze)))
    for row in maze:
        started = False
        for x in range(len(row)):  # for some reason enumerate(row) doesnt work lol
            if row[x * 2].char in ["S", "J", "|", "7", "F", "L"]:
                row.insert(x * 2, MazeChar("|", "P") if started else MazeChar(".", "L"))
                started = True
            else:
                row.insert(x * 2, MazeChar(".", "L"))
                started = False
    return list(map(list, zip(*maze)))


def expand_leaks(maze: list[list[MazeChar]]) -> list[list[MazeChar]]:
    horizontal = horizontal_expand(maze)
    return vertical_expand(horizontal)


def part2() -> int:
    maze = get_data("input")
    x, y = [(x, y) for y, line in enumerate(maze) for x, pipe in enumerate(line) if len(pipe.leads_to) == 4][0]
    maze[y][x].mask = "P"  # dirty fix for starting position
    route = maze[y][x].loop(maze)
    #  get maze mask
    maze_mask: list[list[MazeChar]] = [[pipe.to_maze_char() if Point(x, y) in route else MazeChar(".")
                                        for x, pipe in enumerate(line)]
                                       for y, line in enumerate(maze)]
    #  expand horizontal and vertical, then colour the outside
    expanded_mask = expand_leaks(maze_mask)
    #  fill
    enclosed_mask = expanded_mask.copy()
    flood_fill(enclosed_mask)


    return sum(sum(pipe.mask == "I" for pipe in line) for line in enclosed_mask)


if __name__ == "__main__":
    print("Day 10:")
    # print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
