import math
import itertools
from collections import defaultdict


TEST_RAW = """.#..#
.....
#####
....#
...##""".split('\n')

TEST_SQUARE = [
    [char == '#' for char in line]
    for line in TEST_RAW
]


PART_TWO_RAW = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".split('\n')

PART_TWO_TEST = [[char == '#' for char in line] for line in PART_TWO_RAW]


def in_line_of_sight(station, asteroids, grid_size):
    detected = set()
    for asteroid in asteroids:
        if asteroid != station:
            dx, dy = asteroid[0] - station[0], asteroid[1] - station[1]
            g = abs(math.gcd(dx, dy))
            reduced = (dx//g, dy//g)
            detected.add(reduced)
    return detected


def part_one(square):
    size = (len(TEST_SQUARE[0]), len(TEST_SQUARE))
    asteroids = {
        (x, y)
        for y, row in enumerate(square)
        for x, val in enumerate(row)
        if val
    }
    max_count = 0
    for ast in asteroids:
        in_los = in_line_of_sight(ast, asteroids, size)
        max_count = max(max_count, len(in_los))
    return max_count


def dist_angle_between_asteroids(source, target):
    dx = target[0] - source[0]
    # inverting y because +y is down
    dy = source[1] - target[1]
    dist = math.sqrt(dx ** 2 + dy ** 2)
    angle = math.atan2(dy, dx)
    return angle, dist



def part_two(square):
    size = (len(TEST_SQUARE), len(TEST_SQUARE[0]))
    asteroids = {
        (x, y)
        for y, row in enumerate(square)
        for x, val in enumerate(row)
        if val
    }
    los = []
    for ast in asteroids:
        in_los = in_line_of_sight(ast, asteroids, size)
        los.append((len(in_los), ast, in_los))
    los.sort(reverse=True)
    _, asteroid, in_los = los[0]
    other_asteroids = sorted(
        (dist_angle_between_asteroids(asteroid, other), other)
        for other in asteroids if other != asteroid
    )
    angles = defaultdict(list)
    for (angle, dist), other in other_asteroids:
        angles[angle].append((dist, other))
        angles[angle].sort()
    # pointing up
    initial_angle = math.pi / 2
    angle_list = sorted(angles.items())
    for index, (angle, _) in enumerate(angle_list):
        if angle >= initial_angle:
            # starting here
            break
    
    # let's start destroying
    destroyed = 0
    length = len(angle_list)
    while destroyed < 200:
        
        try:
            _, other = angle_list[index][1][0]
            del angle_list[index][1][0]
        except IndexError:
            if not any(
                i[1] for i in angle_list
            ):
                # This should only happen with the small test case
                print('done!', destroyed)
                x, y = other
                return 100 * x * y
        else:
            destroyed += 1
        # iterating backward through the list because we want to
        # go clockwise
        index -= 1
        index %= length
    
    # ok, we've blown up 200
    x, y = other
    return 100 * x + y


assert part_one(TEST_SQUARE) == 8, part_one(TEST_SQUARE)

with open('input10.txt') as infile:
    real_square = [
        [char == '#' for char in line]
        for line in infile
    ]

print(part_one(real_square))
assert part_two(PART_TWO_TEST) == 802
print(part_two(real_square))