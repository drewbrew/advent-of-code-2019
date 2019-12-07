"""day 5"""
from collections import deque
from itertools import permutations


with open('input7.txt') as infile:
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


def run2(opcodes, phases):
    offsets = [0] * 5
    cpu_inputs = [opcodes[:] for _ in range(5)]
    active_amp = 0
    last_output = 0
    signal_inputs = [deque([i]) for i in phases]
    signal_inputs[0].append(0)
    while True:
        inputs = cpu_inputs[active_amp]
        if not inputs:
            if not any(i for i in cpu_inputs):
                return last_output
            raise RuntimeError('found a dead cpu')
        offset = offsets[active_amp]
        next_opcode = inputs[offset]
        input1_mode = next_opcode // 100 % 10
        input2_mode = next_opcode // 1000 % 10
        output_mode = next_opcode // 10000 % 10
        next_opcode = next_opcode % 100
        if next_opcode == 1:
            add(offset, inputs, input1_mode, input2_mode, output_mode)
            offset += 4
            offsets[active_amp] = offset
        elif next_opcode == 2:
            mul(offset, inputs, input1_mode, input2_mode, output_mode)
            offset += 4
            offsets[active_amp] = offset
        elif next_opcode == 99:
            cpu_inputs[active_amp] = []
            active_amp = (active_amp + 1) % 5
            continue
        elif next_opcode == 3:
            assert not input1_mode
            assert not input2_mode
            assert not output_mode
            store(inputs, inputs[offset + 1], signal_inputs[active_amp])
            offset += 2
            offsets[active_amp] = offset
        elif next_opcode == 4:
            assert not input2_mode
            assert not output_mode
            last_output = retrieve(inputs, inputs[offset + 1], input1_mode)
            offset += 2
            offsets[active_amp] = offset
            active_amp = (active_amp + 1) % 5
            signal_inputs[active_amp].append(last_output)
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
            offsets[active_amp] = offset
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
            offsets[active_amp] = offset
        elif next_opcode == 7:
            less_than(offset, inputs, input1_mode, input2_mode, output_mode)
            offset += 4
            offsets[active_amp] = offset
        elif next_opcode == 8:
            equal(offset, inputs, input1_mode, input2_mode, output_mode)
            offset += 4
            offsets[active_amp] = offset
        else:
            raise ValueError('oh no')


def part_one():
    arrangements = permutations([1, 2, 3, 4, 0], 5)
    last_output = 0
    outputs = []
    for phase_inputs in arrangements:
        last_output = 0
        for phase in phase_inputs:
            inputs = source_inputs[:]
            amp_input = deque([phase, last_output])
            last_output = run(inputs, amp_input)
        outputs.append(last_output)
    return max(outputs)


def part_two():
    arrangements = permutations([5, 6, 7, 8, 9], 5)

    outputs = []
    for phase_inputs in arrangements:
        outputs.append(run2(source_inputs, phase_inputs))
    return max(outputs)

print(part_one())
print(part_two())
