from math import floor

with open('input1.txt') as infile:
    lines = infile.read().split('\n')


inputs = list(int(i.strip()) for i in lines if i.strip())


def fuel(module):
    return floor(module / 3) - 2


def part_two(module):
    needed_fuel = fuel(module)
    total = needed_fuel
    while needed_fuel > 0:
        needed_fuel = max(fuel(needed_fuel), 0)
        total += needed_fuel
    return total


print(sum(fuel(i) for i in inputs))

print(sum(part_two(i) for i in inputs))
