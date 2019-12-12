import math
from collections import defaultdict

TEST_INPUT_1 = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""".split('\n')


TEST_INPUT_2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""".split('\n')



def parse_moon(line):
    line = [i.strip() for i in line[1:-1].split(',')]
    values = tuple(int(i.split('=')[1]) for i in line)
    return Position(*values)


class Position():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.velocity = Velocity(0, 0, 0)

    def generate_gravity(self, other):

        def inner(p1, p2):
            if p1 == p2:
                return 0
            if p1 < p2:
                return 1
            return -1

        gravity = tuple(
            inner(getattr(self, i), getattr(other, i))
            for i in 'xyz'
        )
        return gravity

    def adjust_gravity(self, gravity):
        self.velocity.adjust(gravity)

    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
        self.z += self.velocity.z

    @property
    def potential_energy(self):
        return sum(abs(i) for i in [self.x, self.y, self.z])

    @property
    def kinetic_energy(self):
        return sum(abs(i) for i in [
            self.velocity.x, self.velocity.y, self.velocity.z
        ])
    
    def __str__(self):
        return (
            "pos=<x={self.x}, y={self.y}, z={self.z}>,"
            " vel=<x={self.velocity.x}, y={self.velocity.y},"
            " z={self.velocity.z}> pot={self.potential_energy},"
            " kin={self.kinetic_energy}"
        ).format(self=self)

    def as_tuple(self, dim):
        return (
            getattr(self, dim),
            getattr(self.velocity, dim),
        )


class Velocity():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def adjust(self, gravity):
        self.x += gravity[0]
        self.y += gravity[1]
        self.z += gravity[2]


def run(moons, steps=1000):
    for _ in range(steps):
        gravities = defaultdict(lambda: [0, 0, 0])
        for index, moon in enumerate(moons):
            others = moons[index + 1:]
            for other_i, other in enumerate(others):
                grav = moon.generate_gravity(other)
                gravities[index] = [
                    gravities[index][i] + grav[i]
                    for i in range(3)
                ]
                other_index = index + other_i + 1
                gravities[other_index] =  [
                    gravities[other_index][i] - grav[i]
                    for i in range(3)
                ]
        
        for index, moon in enumerate(moons):
            moon.adjust_gravity(gravities[index])
            moon.move()


def part_one(puzzle, steps=1000):
    moons = [parse_moon(line) for line in puzzle]
    run(moons, steps)
    return sum(
        moon.potential_energy * moon.kinetic_energy
        for moon in moons
    )
    

def lcm(a, b):
    """Calculate the least common multiple without using numpy"""
    return abs(a * b) // math.gcd(a, b)

def part_two(puzzle):
    # The x, y, and z dimensions do not interact at all
    # Therefore, we can loop over each dimension independently
    # and then find the least common multiple of the three
    # dimensions' repeat points to get our answer
    repeats = [0, 0, 0]
    for index, dim in enumerate('xyz'):
        moons = [parse_moon(line) for line in puzzle]
        positions_seen = {tuple(i.as_tuple(dim) for i in moons)}
        steps = 0
        while True:
            steps += 1
            run(moons, 1)
            new_pos = tuple(i.as_tuple(dim) for i in moons)
            if new_pos in positions_seen:
                repeats[index] = steps
                break
            positions_seen.add(new_pos)

    return lcm(lcm(repeats[0], repeats[1]), repeats[2])
    

assert part_one(TEST_INPUT_1, 10) == 179

with open('input12.txt') as infile:
    PUZZLE = [line.strip() for line in infile]

print(part_one(PUZZLE))
assert part_two(TEST_INPUT_1) == 2772
print('starting part two')
print(part_two(PUZZLE))