"""day 5"""
from collections import deque, defaultdict
from itertools import permutations


with open('input11.txt') as infile:
    source_inputs = [int(i) for i in infile.read().split(',')]


def get_offset(inputs, position, mode, relative_base):
    if mode == 0:
        return inputs[position]
    if mode == 1:
        return position
    if mode == 2:
        position = inputs[position]
        return relative_base + position
    raise ValueError(mode)


def add(opcode_position, inputs, input1_mode, input2_mode, output_mode, relative_base):
    offset1 = get_offset(inputs, opcode_position + 1, input1_mode, relative_base)
    offset2 = get_offset(inputs, opcode_position + 2, input2_mode, relative_base)
    offset3 = get_offset(inputs, opcode_position + 3, output_mode, relative_base)
    value1 = inputs[offset1]
    value2 = inputs[offset2]
    inputs[offset3] = value1 + value2


def mul(opcode_position, inputs, input1_mode, input2_mode, output_mode, relative_base):
    offset1 = get_offset(inputs, opcode_position + 1, input1_mode, relative_base)
    offset2 = get_offset(inputs, opcode_position + 2, input2_mode, relative_base)
    offset3 = get_offset(inputs, opcode_position + 3, output_mode, relative_base)
    value1 = inputs[offset1]
    value2 = inputs[offset2]
    inputs[offset3] = value1 * value2


def store(inputs, opcode_position, input_mode, value, relative_base):
    offset = get_offset(inputs, opcode_position + 1, input_mode, relative_base)
    inputs[offset] = value


def retrieve(inputs, opcode_position, input1_mode, relative_base):
    offset1 = get_offset(inputs, opcode_position + 1, input1_mode, relative_base)
    value1 = inputs[offset1]
    return value1


def jump_if_true(inputs, opcode_position, input1_mode, input2_mode, relative_base):
    offset1 = get_offset(inputs, opcode_position + 1, input1_mode, relative_base)
    offset2 = get_offset(inputs, opcode_position + 2, input2_mode, relative_base)
    condition = inputs[offset1]
    destination = inputs[offset2]
    if condition:
        return destination
    return None


def jump_if_false(inputs, opcode_position, input1_mode, input2_mode, relative_base):
    offset1 = get_offset(inputs, opcode_position + 1, input1_mode, relative_base)
    offset2 = get_offset(inputs, opcode_position + 2, input2_mode, relative_base)
    condition = inputs[offset1]
    destination = inputs[offset2]
    if not condition:
        return destination
    return None


def less_than(opcode_position, inputs, input1_mode, input2_mode, output_mode, relative_base):
    offset1 = get_offset(inputs, opcode_position + 1, input1_mode, relative_base)
    offset2 = get_offset(inputs, opcode_position + 2, input2_mode, relative_base)
    offset3 = get_offset(inputs, opcode_position + 3, output_mode, relative_base)
    value1 = inputs[offset1]
    value2 = inputs[offset2]
    inputs[offset3] = int(value1 < value2)


def equal(opcode_position, inputs, input1_mode, input2_mode, output_mode, relative_base):
    offset1 = get_offset(inputs, opcode_position + 1, input1_mode, relative_base)
    offset2 = get_offset(inputs, opcode_position + 2, input2_mode, relative_base)
    offset3 = get_offset(inputs, opcode_position + 3, output_mode, relative_base)
    value1 = inputs[offset1]
    value2 = inputs[offset2]
    inputs[offset3] = int(value1 == value2)


def advance_robot(position, heading, turn):
    if turn:
        heading *= 1j
    else:
        heading *= -1j
    position += heading
    return heading, position



def run(inputs, part_two=False):
    offset = 0
    outputs = {}
    temp_output = None
    relative_base = 0
    position = 0 + 0j
    # invert our coordinates so we don't get an upside down image
    heading = -1j
    new_inputs = defaultdict(lambda: 0)
    for index, i in enumerate(inputs):
        new_inputs[index] = i
    inputs = new_inputs
    while True:
        next_opcode = inputs[offset]
        input1_mode = next_opcode // 100 % 10
        input2_mode = next_opcode // 1000 % 10
        output_mode = next_opcode // 10000 % 10
        next_opcode = next_opcode % 100
        if next_opcode == 1:
            add(offset, inputs, input1_mode, input2_mode, output_mode, relative_base)
            offset += 4
        elif next_opcode == 2:
            mul(offset, inputs, input1_mode, input2_mode, output_mode, relative_base)
            offset += 4
        elif next_opcode == 99:
            return outputs
        elif next_opcode == 3:
            assert not input2_mode
            assert not output_mode
            store(inputs, offset, input1_mode, outputs.get(position, int(part_two)), relative_base)
            offset += 2
        elif next_opcode == 4:
            assert not input2_mode
            assert not output_mode
            last_output = retrieve(inputs, offset, input1_mode, relative_base)
            if temp_output is not None:
                # turn and move
                heading, position = advance_robot(position, heading, last_output)
                temp_output = None
            else:
                # paint!
                outputs[position] = last_output
                temp_output = last_output
            offset += 2
        elif next_opcode == 5:
            next_ip = jump_if_true(
                inputs,
                offset,
                input1_mode,
                input2_mode,
                relative_base,
            )
            if next_ip is not None:
                offset = next_ip
            else:
                offset += 3
        elif next_opcode == 6:
            next_ip = jump_if_false(
                inputs,
                offset,
                input1_mode,
                input2_mode,
                relative_base,
            )
            if next_ip is not None:
                offset = next_ip
            else:
                offset += 3
        elif next_opcode == 7:
            less_than(offset, inputs, input1_mode, input2_mode, output_mode, relative_base)
            offset += 4
        elif next_opcode == 8:
            equal(offset, inputs, input1_mode, input2_mode, output_mode, relative_base)
            offset += 4
        elif next_opcode == 9:
            addr = get_offset(inputs, offset + 1, input1_mode, relative_base)
            relative_base += inputs[addr]
            offset += 2
        else:
            print(next_opcode)
            raise ValueError('oh no')


def part_one():
    paints = run(source_inputs)
    return len(paints)


def part_two():
    paints = run(source_inputs, True)
    columns = [int(i.real) for i in paints]
    rows = [int(i.imag) for i in paints]
    for y in range(min(rows), max(rows) + 1):
        print(
            ''.join(
                '#' if paints.get(x + 1j * y, 0) == 1 else ' '
                for x in range(min(columns), max(columns) + 1)
            )
        )

print(part_one())
part_two()