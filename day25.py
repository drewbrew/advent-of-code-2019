"""day 25: cryostasis


This one is lots of fun. You'll have to manually figure
out what combo of inventory gets you past the gate.
"""
import sys
from collections import deque, defaultdict
from itertools import permutations


with open('input25.txt') as infile:
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


def run(inputs, verbose=False):
    offset = 0
    relative_base = 0
    last_input = []
    
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
            return
        elif next_opcode == 3:
            assert not input2_mode
            if not last_input:
                result = input('')
                if not result.endswith('\n'):
                    result += '\n'
                last_input = [ord(i) for i in result]
            store(inputs, offset, input1_mode, last_input.pop(0), relative_base)
            offset += 2
        elif next_opcode == 4:
            assert not input2_mode
            assert not output_mode
            last_output = retrieve(inputs, offset, input1_mode, relative_base)
            print(chr(last_output), end='')
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
    return run(source_inputs)


print(part_one())