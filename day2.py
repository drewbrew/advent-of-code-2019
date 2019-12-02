"""day 2"""

with open('input2.txt') as infile:
    source_inputs = [int(i) for i in infile.read().split(',')]


def add(opcode_position, inputs):
    offset1 = inputs[opcode_position + 1]
    offset2 = inputs[opcode_position + 2]
    inputs[inputs[opcode_position + 3]] = inputs[offset1] + inputs[offset2]


def mul(opcode_position, inputs):
    offset1 = inputs[opcode_position + 1]
    offset2 = inputs[opcode_position + 2]
    inputs[inputs[opcode_position + 3]] = inputs[offset1] * inputs[offset2]


def run(inputs):
    offset = 0
    while True:
        next_opcode = inputs[offset]
        if next_opcode == 1:
            add(offset, inputs)
        elif next_opcode == 2:
            mul(offset, inputs)
        elif next_opcode == 99:
            return
        else:
            raise ValueError('oh no')
        offset += 4


def part_one():
    inputs = source_inputs[:]
    inputs[1] = 12
    inputs[2] = 2
    run(inputs)
    print(inputs[0])


def part_two():
    for x in range(100):
        for y in range(100):
            inputs = source_inputs[:]
            assert inputs[0] == 1
            inputs[1] = x
            inputs[2] = y
            run(inputs)
            if inputs[0] == 19690720:
                print(x, y, 100 * x + y)
                return


part_one()
part_two()
