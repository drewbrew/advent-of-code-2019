"""day 5"""
from collections import deque


with open('input5.txt') as infile:
    source_inputs = [int(i) for i in infile.read().split(',')]


TEST_INPUT = [
    int(i) for i in
    """3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99""".replace('\n', '').split(',')
]


def add(opcode_position, inputs, input1_mode, input2_mode, output_mode):
    offset1 = inputs[opcode_position + 1]
    offset2 = inputs[opcode_position + 2]
    value1 = offset1 if input1_mode else inputs[offset1]
    value2 = offset2 if input2_mode else inputs[offset2]
    output_offset = opcode_position + 3
    if output_mode:
        inputs[output_offset] = value1 + value2
    else:
        inputs[inputs[output_offset]] = value1 + value2


def mul(opcode_position, inputs, input1_mode, input2_mode, output_mode):
    offset1 = inputs[opcode_position + 1]
    offset2 = inputs[opcode_position + 2]
    value1 = offset1 if input1_mode else inputs[offset1]
    value2 = offset2 if input2_mode else inputs[offset2]
    output_offset = opcode_position + 3
    if output_mode:
        inputs[output_offset] = value1 * value2
    else:
        inputs[inputs[output_offset]] = value1 * value2


def store(inputs, value, rx_buffer):
    store_val = rx_buffer.popleft()
    inputs[value] = store_val


def retrieve(inputs, value, input1_mode):
    return value if input1_mode else inputs[value]


def jump_if_true(inputs, condition, destination, input1_mode, input2_mode):
    if not input1_mode:
        condition = inputs[condition]
    if not input2_mode:
        destination = inputs[destination]
    if condition:
        return destination
    return None


def jump_if_false(inputs, condition, destination, input1_mode, input2_mode):
    if not input1_mode:
        condition = inputs[condition]
    if not input2_mode:
        destination = inputs[destination]
    if not condition:
        return destination
    return None


def less_than(opcode_position, inputs, input1_mode, input2_mode, output_mode):
    offset1 = inputs[opcode_position + 1]
    offset2 = inputs[opcode_position + 2]
    value1 = offset1 if input1_mode else inputs[offset1]
    value2 = offset2 if input2_mode else inputs[offset2]
    output_offset = opcode_position + 3
    if output_mode:
        inputs[output_offset] = int(value1 < value2)
    else:
        inputs[inputs[output_offset]] = int(value1 < value2)


def equal(opcode_position, inputs, input1_mode, input2_mode, output_mode):
    offset1 = inputs[opcode_position + 1]
    offset2 = inputs[opcode_position + 2]
    value1 = offset1 if input1_mode else inputs[offset1]
    value2 = offset2 if input2_mode else inputs[offset2]
    output_offset = opcode_position + 3
    if output_mode:
        inputs[output_offset] = int(value1 == value2)
    else:
        inputs[inputs[output_offset]] = int(value1 == value2)


def run(inputs, program_inputs):
    offset = 0
    last_output = None
    while True:
        next_opcode = inputs[offset]
        input1_mode = next_opcode // 100 % 10
        input2_mode = next_opcode // 1000 % 10
        output_mode = next_opcode // 10000 % 10
        next_opcode = next_opcode % 100
        if next_opcode == 1:
            add(offset, inputs, input1_mode, input2_mode, output_mode)
            offset += 4
        elif next_opcode == 2:
            mul(offset, inputs, input1_mode, input2_mode, output_mode)
            offset += 4
        elif next_opcode == 99:
            return last_output
        elif next_opcode == 3:
            assert not input1_mode
            assert not input2_mode
            assert not output_mode
            store(inputs, inputs[offset + 1], program_inputs)
            offset += 2
        elif next_opcode == 4:
            assert not input2_mode
            assert not output_mode
            last_output = retrieve(inputs, inputs[offset + 1], input1_mode)
            offset += 2
        elif next_opcode == 5:
            next_ip = jump_if_true(
                inputs,
                inputs[offset + 1],
                inputs[offset + 2],
                input1_mode,
                input2_mode,
            )
            if next_ip is not None:
                offset = next_ip
            else:
                offset += 3
        elif next_opcode == 6:
            next_ip = jump_if_false(
                inputs,
                inputs[offset + 1],
                inputs[offset + 2],
                input1_mode,
                input2_mode,
            )
            if next_ip is not None:
                offset = next_ip
            else:
                offset += 3
        elif next_opcode == 7:
            less_than(offset, inputs, input1_mode, input2_mode, output_mode)
            offset += 4
        elif next_opcode == 8:
            equal(offset, inputs, input1_mode, input2_mode, output_mode)
            offset += 4
        else:
            print(next_opcode)
            raise ValueError('oh no')


def part_one():
    inputs = source_inputs[:]
    print(run(inputs, deque([1])))


def part_two():
    test_low = run(TEST_INPUT, deque([7]))
    assert test_low == 999
    test_8 = run(TEST_INPUT, deque([8]))
    assert test_8 == 1000
    test_high = run(TEST_INPUT, deque([9]))
    assert test_high == 1001
    inputs = source_inputs[:]
    print(run(inputs, deque([5])))


part_one()
part_two()
