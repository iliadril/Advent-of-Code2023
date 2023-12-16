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

    def loop(self, maze: list[list['MazeTile']]):
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
                current_pipe.mask = "P"  # TODO check whether only route pipes needs to be marked
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


def mask_outside(maze: list[list[MazeTile]]):
    for y, line in enumerate(maze):
        for x, pipe in enumerate(line):
            if pipe.mask != "P":
                if y == 0 or y == len(maze) - 1 or x == 0 or x == len(maze[0]) - 1:
                    pipe.mask = "O"
                    continue
                if any(maze[j][i].mask == "O" for i, j in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]):
                    pipe.mask = "O"


def horizontal_expand(maze: list[list[MazeChar]]):
    length, height = len(maze[0]), len(maze)
    for row in maze:
        x = 0
        started = False
        while x < length:
            if row[x * 2].char in ["S", "J", "-", "7", "F", "L"]:
                if row[x * 2 - 1].char in ["7", "J"]:
                    row.insert(x * 2, MazeChar("-", "P") if not started else MazeChar(".", "L"))
                else:
                    row.insert(x * 2, MazeChar("-", "P") if started else MazeChar(".", "L"))
                started = True
            else:
                row.insert(x * 2, MazeChar(".", "L"))
                started = False
            x += 1


def expand_leaks(maze: list[list[MazeChar]]):
    x, y = 1, 1
    while y < len(maze) and x < len(maze[0]):
        current_tile = maze[y][x]


def part2() -> int:
    maze = get_data("test_input_part2")
    x, y = [(x, y) for y, line in enumerate(maze) for x, pipe in enumerate(line) if len(pipe.leads_to) == 4][0]
    _ = maze[y][x].loop(maze)
    # expand vertically
    maze_mask: list[list[MazeChar]] = [[pipe.to_maze_char() for pipe in line] for line in maze]

    for line in maze_mask:
        for mask in line:
            print(mask.char, sep="", end="")
        print()

    horizontal_expand(maze_mask)
    for line in maze_mask:
        for mask in line:
            print(mask.char, sep="", end="")
        print()

    return sum(sum(pipe.mask == "I" for pipe in line) for line in maze)


if __name__ == "__main__":
    print("Day 10:")
    # print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
