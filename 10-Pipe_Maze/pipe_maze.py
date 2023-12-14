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


class MazeTile:
    position: Point
    leads_to: list[Point]

    def __init__(self, position: Point, char: str):
        self.position = position
        self.leads_to = [output + position for output in Point.from_char(char)]

    def is_valid_route(self, target: Point, maze: list[list['MazeTile']]):
        return target in self.leads_to and self.position in maze[target.y][target.x].leads_to

    def loop(self, maze: list[list['MazeTile']]):
        current_pipe = self
        route = [self.position]
        while bool(len(route) == 1) != bool(current_pipe != self):
            possibilities = [[x, y] for x, y in current_pipe.leads_to
                             if current_pipe.is_valid_route(Point(x, y), maze) and Point(x, y) not in route]
            if not possibilities:
                # route += [self.position]
                break
            for x, y in possibilities:
                current_pipe = maze[y][x]
                route += [Point(x, y)]
                break
        return route

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


def part2() -> int:
    return


if __name__ == "__main__":
    print("Day 10:")
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
