"""Day 24: Game of life"""

TEST_INPUT = """....#
#..#.
#..##
..#..
#....""".split('\n')


def parse_input(lines: list, part_two: bool = False) -> set:
    grid = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                if part_two:
                    if (x, y) == (2, 2):
                        continue
                    grid.add((x, y, 0))
                else:
                    grid.add((x, y))
    return grid


assert parse_input(TEST_INPUT) == {
    (4, 0),
    (0, 1),
    (3, 1),
    (0, 2),
    (3, 2),
    (4, 2),
    (2, 3),
    (0, 4),
}, parse_input(TEST_INPUT)


def take_turn(grid: set) -> set:
    new_grid = set()
    for y in range(5):
        for x in range(5):
            neighbors = {
                (dx, dy)
                for (dx, dy) in {
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1),
                }
                if (dx, dy) in grid
            }
            # print(x, y, neighbors)
            if (x, y) in grid:
                # if a bug currently occupies this spot,
                # it dies UNLESS there is exactly one bug
                # next to it
                # print('occupied')
                if len(neighbors) == 1:
                    # print('stay alive')
                    new_grid.add((x, y))
            else:
                # if a spot is unoccupied, it only spawns
                # IF there are 1-2 bugs next to it
                # print('open')
                if len(neighbors) in {2, 1}:
                    # print('spawn')
                    new_grid.add((x, y))
    return new_grid


assert take_turn(parse_input(TEST_INPUT)) == {
    (0, 0),
    (3, 0),
    (0, 1),
    (1, 1),
    (2, 1),
    (3, 1),
    (0, 2),
    (1, 2),
    (2, 2),
    (4, 2),
    (0, 3),
    (1, 3),
    (3, 3),
    (4, 3),
    (1, 4),
    (2, 4),
}, take_turn(parse_input(TEST_INPUT))


def biodiversity(grid: set) -> int:
    return sum(
        2 ** (y * 5 + x)
        for (x, y) in grid
    )


assert biodiversity({(0, 3), (1, 4)}) == 2129920, biodiversity(
    {(0, 3), (1, 4)}
)


def display_grid(grid: set, z: int = None):
    for y in range(5):
        for x in range(5):
            if z is not None:
                present = (x, y, z) in grid
            else:
                present = (x, y) in grid
            if present:
                print('#', end='')
            else:
                print('.', end='')
        print('')


def part_one(puzzle_input: str) -> int:
    grid = parse_input(puzzle_input)
    grids_seen = set()
    grids_seen.add(tuple(sorted(grid)))
    iterations = 0
    while True:
        iterations += 1
        new_grid = take_turn(grid)
        check = tuple(sorted(new_grid))
        if check in grids_seen:
            print(f'Found repeat after {iterations} turns')
            display_grid(new_grid)
            return biodiversity(new_grid)
        grids_seen.add(check)
        grid = new_grid


assert part_one(TEST_INPUT) == 2129920


def p2_neighbors(x: int, y: int, z: int) -> set:
    neighbors = set()
    for (dx, dy) in {
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    }:
        dz = z
        if (dx, dy) == (2, 2):
            # need to go in one layer
            dz += 1
            # what direction did we come from?
            if x == 1:
                # we came in from the left
                # so we need to add all five left tiles
                # on that level
                neighbors |= set([
                    (0, ddy, dz) for ddy in range(5)
                ])
            elif y == 1:
                # came in from the top
                neighbors |= set([
                    (ddx, 0, dz) for ddx in range(5)
                ])
            elif x == 3:
                # came in from the right
                neighbors |= set([
                    (4, ddy, dz) for ddy in range(5)
                ])
            elif y == 3:
                # came in from the bottom
                neighbors |= set([
                    (ddx, 4, dz) for ddx in range(5)
                ])
            else:
                raise ValueError('all points equal?!')
        elif dx == -1:
            # need to go out one layer
            dz -= 1
            # and pick (1, 2) from that layer
            neighbors.add((1, 2, dz))
        elif dx == 5:
            # out one layer and (3, 2)
            dz -= 1
            neighbors.add((3, 2, dz))
        elif dy == 5:
            # out one layer and (2, 3)
            dz -= 1
            neighbors.add((2, 3, dz))
        elif dy == -1:
            # out one layer and (2, 1)
            dz -= 1
            neighbors.add((2, 1, dz))
        else:
            # same layer
            neighbors.add((dx, dy, dz))
    z_values = (i[2] for i in neighbors)
    assert all(
        (2, 2, z) not in neighbors for z in z_values
    ), neighbors
    return neighbors


assert p2_neighbors(1, 1, 0) == {
    (0, 1, 0),
    (1, 0, 0),
    (2, 1, 0),
    (1, 2, 0),
}

assert p2_neighbors(1, 2, 0) == {
    (0, 2, 0),
    (1, 1, 0),
    (1, 3, 0),
    # enter next layer from the top
    (0, 0, 1),
    (0, 1, 1),
    (0, 2, 1),
    (0, 3, 1),
    (0, 4, 1),
}

assert p2_neighbors(3, 2, 0) == {
    (3, 3, 0),
    (3, 1, 0),
    (4, 2, 0),
    # enter next layer from the right
    (4, 0, 1),
    (4, 1, 1),
    (4, 2, 1),
    (4, 3, 1),
    (4, 4, 1),
}

assert p2_neighbors(2, 1, 0) == {
    (1, 1, 0),
    (3, 1, 0),
    (2, 0, 0),
    # enter next layer from the top
    (0, 0, 1),
    (1, 0, 1),
    (2, 0, 1),
    (3, 0, 1),
    (4, 0, 1),
}

assert p2_neighbors(2, 3, 0) == {
    (1, 3, 0),
    (2, 4, 0),
    (3, 3, 0),
    # enter next layer from below
    (0, 4, 1),
    (1, 4, 1),
    (2, 4, 1),
    (3, 4, 1),
    (4, 4, 1),
}, sorted(p2_neighbors(2, 3, 0))


assert p2_neighbors(0, 1, 0) == {
    (1, 1, 0),
    (0, 0, 0),
    (0, 2, 0),
    (1, 2, -1),
}


assert p2_neighbors(0, 0, 0) == {
    (1, 0, 0),
    (0, 1, 0),
    (1, 2, -1),
    (2, 1, -1),
}, p2_neighbors(0, 0, 0)


assert p2_neighbors(4, 0, 0) == {
    (3, 0, 0),
    (4, 1, 0),
    (2, 1, -1),
    (3, 2, -1),
}, p2_neighbors(4, 0, 0)

assert p2_neighbors(0, 4, 0) == {
    (0, 3, 0),
    (1, 4, 0),
    (1, 2, -1),
    (2, 3, -1),
}, p2_neighbors(0, 4, 0)

assert p2_neighbors(4, 4, 0) == {
    (3, 4, 0),
    (4, 3, 0),
    (2, 3, -1),
    (3, 2, -1),
}


def take_turn_p2(grid: set) -> set:
    new_grid = set()
    z_values = sorted(i[2] for i in grid)
    min_z = z_values[0]
    max_z = z_values[-1]
    # print(min_z, max_z)
    for z in range(min_z - 1, max_z + 2):
        assert (2, 2, z) not in grid
        # print('z', z)
        for y in range(5):
            for x in range(5):
                if (x, y) == (2, 2):
                    # I'll handle that when I get to the next layer
                    continue
                neighbors = {
                    coord
                    for coord in p2_neighbors(x, y, z)
                    if coord in grid
                }
                # print(x, y, z, neighbors)
                
                if (x, y, z) in grid:
                    # if a bug currently occupies this spot,
                    # it dies UNLESS there is exactly one bug
                    # next to it
                    # print('occupied')
                    if len(neighbors) == 1:
                        # print('stay alive')
                        new_grid.add((x, y, z))
                else:
                    # if a spot is unoccupied, it only spawns
                    # IF there are 1-2 bugs next to it
                    # print('open')
                    if len(neighbors) in {2, 1}:
                        # print('spawn')
                        new_grid.add((x, y, z))
    return new_grid


def part_two(puzzle_input: str, turns: int = 200) -> int:
    grid = parse_input(puzzle_input, True)
    for turn in range(turns):
        if not turn % 10:
            print(turn, len(grid))
        if not grid:
            raise ValueError(f'All dead before turn {turn}')
        grid = take_turn_p2(grid)
    if turns == 10:
        success = True
        for z, expected_grid in EXPECTED_P2_GRIDS.items():

            layer = {(x, y) for (x, y, dz) in grid if z == dz}
            if layer != expected_grid:
                success = False
                print(f'Mismatch at depth {z}; got:')
                display_grid(layer)
        assert success
    return len(grid)


EXPECTED_P2_GRIDS = {
    -5: parse_input("""..#..
.#.#.
..?.#
.#.#.
..#..""".split('\n')),
    -4: parse_input(
        """...#.
...##
..?..
...##
...#.""".split('\n')
    ),
    -3: parse_input(
        """#.#..
.#...
..?..
.#...
#.#..""".split('\n')
    ),
    -2: parse_input(
        """.#.##
....#
..?.#
...##
.###.""".split('\n')
    ),
    -1: parse_input(
        """#..##
...##
..?..
...#.
.####""".split('\n')
    ),
    0: parse_input(
        """.#...
.#.##
.#?..
.....
.....""".split('\n')
    ),
    1: parse_input(
        """.##..
#..##
..?.#
##.##
#####""".split('\n')
    ),
    2: parse_input(
        """###..
##.#.
#.?..
.#.##
#.#..""".split('\n')
    ),
    3: parse_input(
        """..###
.....
#.?..
#....
#...#""".split('\n')
    ),
    4: parse_input(
        """.###.
#..#.
#.?..
##.#.
.....""".split('\n')
    ),
    5: parse_input(
        """####.
#..#.
#.?#.
####.
.....""".split('\n')
    ),
}

p2_test = part_two(TEST_INPUT, 10)
assert p2_test == 99, p2_test

with open('input24.txt') as infile:
    puzzle_input = [line for line in infile]


print('part 1:', part_one(puzzle_input))
print('part 2:', part_two(puzzle_input))
