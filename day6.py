
with open('input6.txt') as infile:
    lines = [line.strip().split(')') for line in infile if line]



def parse_graph(inputs):
    input_map = {
        source: dest for dest, source in inputs
    }
    return input_map


def dist_to_center(graph, node, dist=0):
    orbiting = graph[node]
    dist += 1
    if orbiting != 'COM':
        return dist_to_center(graph, orbiting, dist)
    return dist


def part_one(graph):
    return sum(dist_to_center(graph, i) for i in graph)


def path_to_node(graph, node, target='COM', path=None):
    if not path:
        path = []
    next_hop = graph[node]
    path.append(next_hop)
    if next_hop == target:
        return path
    return path_to_node(graph, next_hop, target, path)


def part_two(graph):
    my_path = path_to_node(graph, 'YOU')
    santa_path = path_to_node(graph, 'SAN')
    my_rev = list(reversed(my_path))
    santa_rev = list(reversed(santa_path))
    for index, (my_hop, santa_hop) in enumerate(zip(my_rev, santa_rev)):
        if my_hop != santa_hop:
            print('divergence at', index, my_hop, santa_hop)
            break
    my_index = len(my_path) - index
    santa_index = len(santa_path) - index
    return my_index + santa_index


graph = parse_graph(lines)

print(part_one(graph))
print(part_two(graph))