from collections import defaultdict
from math import ceil


TEST_INPUT = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""".split('\n')


def format_material(material):
    mat = material.split(' ')
    return int(mat[0]), mat[1]


def parse_inputs(inputs):
    splits = [line.strip().split(' => ') for line in inputs]
    raw = [
        (eq_inputs.split(', '), output)
        for eq_inputs, output in splits
    ]
    # make sure we have no duplicate outputs
    assert len(set(format_material(i[1])[1] for i in raw)) == len(raw)
    output = {}
    for sources, target in raw:
        target_qty, target_material = format_material(target)
        output[target_material] = (target_qty, [
            format_material(source) for source in sources
        ])
    return output


def minimum_ore(reactions, chem='FUEL', units=1, waste=None):

    if waste is None:
        waste = defaultdict(int)
    
    if chem == 'ORE':
        return units
    
    # Re-use waste chemicals.
    reuse = min(units, waste[chem])
    units -= reuse
    waste[chem] -= reuse

    # Work out how many reactions we need to perform.
    produced, inputs = reactions[chem]
    n = ceil(units / produced)

    # Determine the minimum ore required to produce each input.
    ore = 0
    for required, input in inputs:
        ore += minimum_ore(reactions, input, n * required, waste)

    # Store waste so it can be re-used
    waste[chem] += n * produced - units
    return ore


def part_one(inputs):
    mfg_dict = parse_inputs(inputs)
    return minimum_ore(mfg_dict)


def part_two(inputs):
    mfg_dict = parse_inputs(inputs)
    target = int(1e12)
    lower = None
    upper = 1

    # find our upper bound
    while minimum_ore(mfg_dict, units=upper) < target:
        lower = upper
        upper *= 2

    # then use binary search to find lower bound
    while upper > lower + 1:
        midpoint = (lower + upper) // 2
        ore = minimum_ore(mfg_dict, units=midpoint)
        if ore > target:
            upper = midpoint
        elif ore < target:
            lower = midpoint
    
    return lower

assert part_one(TEST_INPUT) == 2210736, part_one(TEST_INPUT)

with open('input14.txt') as infile:
    real_input = [line for line in infile]


print(part_one(real_input))
assert part_two(TEST_INPUT) == 460664, part_two(TEST_INPUT)
print(part_two(real_input))