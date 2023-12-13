from dataclasses import dataclass


@dataclass
class Race:
    time: int
    target_distance: int

    def max_distance(self) -> int:
        speed = self.time // 2
        return speed * (self.time - speed)

    def possibilities(self):
        return

    def boat_travel(self, hold_time: int) -> int:
        run_time = self.time - hold_time
        return hold_time * run_time

    def brute_force(self) -> int:
        possible = 0
        for hold_time in range(self.time):
            distance = self.boat_travel(hold_time)
            if distance > self.target_distance:
                possible += 1
        return possible


# ~~~~~~~~ END OF CLASSES ~~~~~~~~


def get_data(filename: str) -> list[Race]:
    with open(filename, "r") as f:
        times = f.readline().split(":")[1].strip().split()
        distances = f.readline().split(":")[1].strip().split()
        races = [Race(int(time), int(dist)) for time, dist in zip(times, distances)]
        return races


def part1() -> int:
    races = get_data("input")
    result = 1
    for race in races:
        result *= race.brute_force()
    return result


if __name__ == "__main__":
    print("Day 6:")
    print(part1())
