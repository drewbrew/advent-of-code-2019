import string

with open('input18.txt') as infile:
    lines = [i.strip() for i in infile]


KEYS = string.ascii_lowercase


def dists_from(source, maze):
    """Find the distance from a source to all other nodes it can reach"""
    x, y = source
    visited = {(x, y)}
    # as we traverse points, the third item (distance) will increase
    # and the route will grow, e.g. aBAcDdQfx
    queue = [(x, y, 0, '')]
    route_info = {}

    for x, y, dist, route in queue:
        contents = maze[y][x]
        if contents not in '.@#1234' and dist > 0:
            # I'm using 1/2/3/4 for the four start points in part two
            # so we can maintain unique points in the dict

            # we found a point of interest! Save it to the route
            route_info[contents] = (dist, route)
            route += contents

        visited.add((x, y))

        for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            # look up, down, left, and right, but only if we haven't seen
            # that point before
            new_x = x + dx
            new_y = y + dy
            if maze[new_y][new_x] != '#' and (new_x, new_y) not in visited:
                queue.append((new_x, new_y, dist + 1, route))

    return route_info


def find_route_info(maze):
    route_info = {}
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char in KEYS + '@1234':
                route_info[char] = dists_from((x, y), maze)
    return route_info


def part_one(maze):
    route_info = find_route_info(maze)
    keys = frozenset(k for k in route_info.keys() if k in KEYS)
    # route is of the form (source point: set(nodes seen)): distance traveled
    info = {('@', frozenset()): 0}
    for dummy in range(len(keys)):
        next_info = {}
        for (location, current_keys), current_dist in info.items():
            for new_key in keys:
                if new_key not in current_keys:
                    # haven't seen this node before!
                    dist, route = route_info[location][new_key]
                    reachable = all(
                        c.casefold() in current_keys
                        for c in route
                    )
                    if reachable:
                        new_dist = dist + current_dist
                        new_keys = frozenset(current_keys | {new_key})

                        dict_key = new_key, new_keys
                        # did we find a new or shorter path that covers all these
                        # nodes?
                        if dict_key not in next_info or new_dist < next_info[dict_key]:
                            # YES! save it
                            next_info[new_key, new_keys] = new_dist
        info = next_info
    return min(info.values())


def transform_for_part_two(maze):
    maze = [list(i) for i in maze]
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == '@':
                maze[y - 1][x - 1] = '1'
                maze[y + 1][x + 1] = '2'
                maze[y + 1][x - 1] = '3'
                maze[y - 1][x + 1] = '4'
                maze[y][x + 1] = '#'
                maze[y][x - 1] = '#'
                maze[y + 1][x] = '#'
                maze[y - 1][x] = '#'
                maze[y][x] = '#'
    return maze


def part_two(maze):
    updated = transform_for_part_two(maze)

    route_info = find_route_info(updated)
    keys = frozenset(k for k in route_info.keys() if k in KEYS)

    # this is basically the same as part 1, only we have four source nodes
    info = {
        (
            ('1', '2', '3', '4'),
            frozenset(),
        ): 0,
    }

    for dummy in range(len(keys)):
        next_info = {}
        for (current_locations, current_keys), current_distance in info.items():
            for new_key in keys:
                if new_key not in current_keys:
                    # also we have to iterate over the four bots for each step
                    # so this takes slightly longer
                    for bot in range(4):
                        if new_key in route_info[current_locations[bot]]:
                            distance, route = route_info[current_locations[bot]][new_key]
                            reachable = all(
                                c.casefold() in current_keys for c in route
                            )

                            if reachable:
                                new_dist = current_distance + distance
                                new_keys = frozenset(current_keys | {new_key})
                                new_locations = list(current_locations)
                                new_locations[bot] = new_key
                                new_locations = tuple(new_locations)

                                if (
                                    new_locations, new_keys,
                                ) not in next_info or new_dist < next_info[
                                    (new_locations, new_keys)
                                ]:
                                    next_info[(new_locations, new_keys)] = new_dist
        info = next_info
    return min(info.values())


print(part_one(lines))
print(part_two(lines))
