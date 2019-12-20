"""Day 20"""
import string
from collections import defaultdict, deque

import networkx


TEST_INPUT_SHORT = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """
            
SHORT_ANSWER = 23

LONG_ANSWER = 58

TEST_INPUT_LONG = """                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """


PART_TWO_TEST = """             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """

TEST_TWO_ANSWER = 396


def parse_puzzle(text: str, part_two: bool = False) -> tuple:
    lines = [i for i in text.split('\n')]
    # parse line by line
    # check every time we hit an alpha char
    # if adjacent (forward or down only) is also alpha,
    # we have portal
    # set up portal dict with {label: [points]}
    # AA and ZZ will only have one (x, y) point as a tuple
    portals = defaultdict(list)
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            entry = None
            exit_ = None
            if char in string.ascii_uppercase:
                try:
                    right = row[x + 1]
                    if right not in string.ascii_uppercase:
                        raise IndexError('foo')
                except IndexError:
                    try:
                        down = lines[y + 1][x]
                        if down not in string.ascii_uppercase:
                            raise IndexError('foo')
                    except IndexError:
                        continue
                    else:
                        if down not in string.ascii_uppercase:
                            continue
                        name = f'{char}{down}'
                        entry = (x, y)
                        if y == 0:
                            exit_ = (x, y + 2)
                            entry = (x, y + 1)
                        else:
                            if lines[y - 1][x] == '.':
                                exit_ = (x, y - 1)
                            else:
                                entry = (x, y + 1)
                                exit_ = (x, y + 2)
                else:
                    if right not in string.ascii_uppercase:
                        continue
                    name = f'{char}{right}'
                    entry = (x, y)
                    if x == 0:
                        exit_ = (x + 2, y)
                        entry = (x + 1, y)
                    else:
                        if lines[y][x - 1] == '.':
                            exit_ = (x - 1, y)
                        else:
                            entry = (x + 1, y)
                            exit_ = (x + 2, y)
                assert entry is not None
                assert exit_ is not None
                if part_two:
                    entry = exit_
                portals[name].append((entry, exit_))
    # ok, we're done iterating over the puzzle
    # now let's build our points for easy handling
    points = {}
    for name, pairs in portals.items():
        if name in ['AA', 'ZZ']:
            assert len(pairs) == 1
            # don't put them in the dict
            continue
        assert len(pairs) == 2, (name, pairs)
        (entry1, exit2), (entry2, exit1) = pairs
        assert entry1 not in points
        assert entry2 not in points
        points[entry1] = exit1
        points[entry2] = exit2
    start = portals['AA'][0][1]
    end = portals['ZZ'][0][1]
    return lines, points, start, end


def part_one(puzzle, warp_points, start, end):
    # For part 1, a simple breadth-first search works
    x, y = start
    queue = deque([(x, y, 0)])
    points_seen = {}

    while True:
        try:
            x, y, dist = queue.popleft()
        except IndexError:
            break
        if (x, y) in points_seen:
            # did we find a faster way to get here
            old_dist = points_seen[(x, y)]
            if dist < old_dist:
                if end == (x, y):
                points_seen[x, y] = dist
            continue
        points_seen[x, y] = dist
        if end == (x, y):
            continue
        for delta_x, delta_y in [
            (1, 0), (-1, 0), (0, 1), (0, -1)
        ]:
            try:
                new_pt = puzzle[y + delta_y][x + delta_x]
            except IndexError:
                continue
            if new_pt == '.':
                queue.append((x + delta_x, y + delta_y, dist + 1))
            elif new_pt == '#':
                # found a wall
                continue
            else:
                try:
                    new_x, new_y = warp_points[(x + delta_x, y + delta_y)]
                except KeyError:
                    if (delta_x + x, delta_y + y) == end:
                        queue.append((delta_x + x, delta_y + y, dist + 1))
                    else:
                        if new_pt == 'A':
                            # at start
                            continue
                        raise ValueError('Oh no')
                else:
                    queue.append((new_x, new_y, dist + 1))
    return points_seen[end]
    

def part_two(puzzle, warps, start, end):
    # for part two, we need to go with Dijkstra since the
    # recursion makes the BFS infeasible
    graph = networkx.Graph()
    levels = 30
    width = max(len(i) for i in puzzle)
    height = len(puzzle)
    for y in range(height):
        for x in range(width):
            if puzzle[y][x] == '.':
                for level in range(levels):
                    graph.add_node((x, y, level))
                neighbors = [
                    (dx + x, dy + y)
                    for dx, dy in [
                        (0, 1), (0, -1), (1, 0), (-1, 0)
                    ] if puzzle[dy + y][dx + x] == '.'
                ]
                for dx, dy in neighbors:
                    for layer in range(levels):
                        graph.add_edge((x, y, layer), (dx, dy, layer))

    for source, target in warps.items():
        if source[0] in [2, width - 3] or source[1] in [2, height - 3]:
            # we have an outer edge
            inner = target
            outer = source
        else:
            outer = target
            inner = source
        for layer in range(levels - 1):
            graph.add_edge((inner[0], inner[1], layer), (outer[0], outer[1], layer + 1))
            graph.add_edge((outer[0], outer[1], layer + 1), (inner[0], inner[1], layer))
    
    for (x1, y1, z1), (x2, y2, z2) in graph.edges:
        assert (x1, y1, z1) in graph.nodes, (x1, y1, z1)
        assert (x2, y2, z2) in graph.nodes, (x2, y2, z2)
    assert start + (0, ) in graph.nodes
    assert end + (0, ) in graph.nodes

    result = networkx.shortest_path_length(
        graph,
        (start[0], start[1], 0),
        (end[0], end[1], 0)
    )
    return result


puzzle, warps, start, end = parse_puzzle(TEST_INPUT_SHORT)
short_result = part_one(puzzle, warps, start, end)
assert short_result == SHORT_ANSWER, short_result
puzzle, warps, start, end = parse_puzzle(TEST_INPUT_SHORT, True)
short_result = part_two(puzzle, warps, start, end)
assert short_result == 26, short_result

puzzle, warps, start, end = parse_puzzle(TEST_INPUT_LONG)
long_result = part_one(puzzle, warps, start, end)
assert long_result == LONG_ANSWER, long_result

puzzle, warps, start, end = parse_puzzle(PART_TWO_TEST, True)
test_result = part_two(puzzle, warps, start, end)
assert test_result == TEST_TWO_ANSWER, test_result

with open('input20.txt') as infile:
    lines = infile.read()


puzzle, warps, start, end = parse_puzzle(lines)
print(part_one(puzzle, warps, start, end))
puzzle, warps, start, end = parse_puzzle(lines, True)
print(part_two(puzzle, warps, start, end))

