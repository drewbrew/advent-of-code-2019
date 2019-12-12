TEST_INPUTS = [
    line.split(',') for line in
    "R75,D30,R83,U83,L12,D49,R71,U7,L72\n"
    "U62,R66,U55,R34,D71,R55,D58,R83".split('\n')
]


with open('input3.txt') as infile:
    steps = [line.split(',') for line in infile]


assert len(steps) == 2


def trace_path(path):
    my_path = [(0, 0)]
    for step in path:
        heading = step[0]
        magnitude = int(step[1:])
        assert heading in 'URLD'
        x, y = my_path[-1]
        if heading == 'U':
            my_path += [
                (x, new_y) for new_y in range(y + 1, y + magnitude + 1)
            ]
        elif heading == 'R':
            my_path += [
                (new_x, y) for new_x in range(x + 1, x + magnitude + 1)
            ]
        elif heading == 'D':
            my_path += [
                (x, new_y) for new_y in range(y - 1, y - magnitude - 1, -1)
            ]
        elif heading == 'L':
            my_path += [
                (new_x, y) for new_x in range(x - 1, x - magnitude - 1, -1)
            ]
    return my_path


def intersections(paths, part_two=False):
    base = set(paths[0]).intersection(paths[1])
    try:
        base.remove((0, 0))
    except KeyError:
        pass
    if part_two:
        result = [
            (point, paths[0].index(point) + paths[1].index(point))
            for point in base
        ]
        return sorted(result, key=lambda k: k[1])
    return sorted(base, key=lambda c: abs(c[0]) + abs(c[1]))


def part_one(paths):
    traced = [trace_path(i) for i in paths]
    crosses = intersections(traced)
    closest = crosses[0] if crosses[0] != (0, 0) else crosses[1]
    print(
        f'Closest intersection is {closest}, dist '
        f'{abs(closest[0]) + abs(closest[1])}'
    )
    return closest


def part_two(paths):
    traced = [trace_path(i) for i in paths]
    crosses = intersections(traced, True)
    closest = crosses[0]
    print(closest[1])
    return closest


test_result = part_one(TEST_INPUTS)
assert abs(test_result[0]) + abs(test_result[1]) == 159, test_result
part_one(steps)
test_result = part_two(TEST_INPUTS)
assert test_result[1] == 610, test_result
part_two(steps)
