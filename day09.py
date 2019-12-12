"""day 5"""
from collections import deque, defaultdict
from itertools import permutations


with open('input9.txt') as infile:
    source_inputs = [int(i) for i in infile.read().split(',')]

TEST_INPUT = [
    int(i) for i in
    "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(',')
]
TEST_INPUT_16 = [
    int(i) for i in
    """1102,34915192,34915192,7,4,7,99,0""".split(',')
]
TEST_RESULT_16 = 1219070632396864


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


def store(inputs, opcode_position, input_mode, rx_buffer, relative_base):
    offset = get_offset(inputs, opcode_position + 1, input_mode, relative_base)
    store_val = rx_buffer.popleft()
    inputs[offset] = store_val


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


def run(inputs, program_inputs):
    offset = 0
    last_output = None
    relative_base = 0
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
            return last_output
        elif next_opcode == 3:
            assert not input2_mode
            assert not output_mode
            store(inputs, offset, input1_mode, program_inputs, relative_base)
            offset += 2
        elif next_opcode == 4:
            assert not input2_mode
            assert not output_mode
            last_output = retrieve(inputs, offset, input1_mode, relative_base)
            print(last_output)
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
    run(source_inputs, deque([1]))


def part_two():
    run(source_inputs, deque([2]))


assert run(TEST_INPUT_16, deque([])) == TEST_RESULT_16
run(TEST_INPUT, deque([]))
print('---')
part_one()
print('===')
part_two()