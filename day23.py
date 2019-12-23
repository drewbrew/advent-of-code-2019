"""day 23: intcode network"""
import sys
from collections import deque, defaultdict
from itertools import permutations


with open('input23.txt') as infile:
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


def run(inputs, computers=50, part_two=False, verbose=False):
    offsets = [0 for _ in range(computers)]
    relative_bases = [0 for _ in range(computers)]
    
    instructions = []
    for computer in range(computers):
        new_inputs = defaultdict(lambda: 0)
        for index, i in enumerate(inputs):
            new_inputs[index] = i
        instructions.append(new_inputs)
    assert len(set(id(i) for i in instructions)) == computers
    cpu_inputs = [
        deque([i]) for i in range(computers)
    ]
    temp_outputs = [
        [] for _ in range(computers)
    ]
    terminated = [False] * computers
    blocked = [False] * computers
    nat_buffer = []
    last_nat_sent = []
    while True:
        for computer in range(computers):
            if terminated[computer]:
                if all(terminated):
                    print('Everything is done')
                    return
                continue
            if all(blocked) and part_two:
                try:
                    x, y = nat_buffer
                except ValueError:
                    if verbose:
                        print('all idle, nothing to send')
                else:
                    if verbose:
                        print(f'all idle, sending {x}, {y}')
                    if nat_buffer == last_nat_sent:
                        print(f'Part 2 solution {x}, {y}')
                        return y
                    cpu_inputs[0].extend(nat_buffer)
                    last_nat_sent = nat_buffer
                    nat_buffer = []
            inputs = instructions[computer]
            offset = offsets[computer]

            relative_base = relative_bases[computer]
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
                terminated[computer] = True
            elif next_opcode == 3:
                assert not input2_mode
                try:
                    value = cpu_inputs[computer].popleft()
                except IndexError:
                    value = -1
                    blocked[computer] = True
                else:
                    blocked[computer] = False
                    # print(f'cpu {computer}: received {value}; {cpu_inputs}')
                store(inputs, offset, input1_mode, value, relative_base)
                offset += 2
            elif next_opcode == 4:
                assert not input2_mode
                assert not output_mode
                last_output = retrieve(inputs, offset, input1_mode, relative_base)
                temp_output = temp_outputs[computer]
                if len(temp_output) < 2:
                    if verbose:
                        print(f'{computer} sent {last_output}, temp {temp_output}')
                    temp_output.append(last_output)
                else:
                    dest, x = temp_output
                    temp_output.clear()
                    y = last_output
                    if dest == 255:
                        if not part_two:
                            print('255!', x, y)
                            return y
                        else:
                            nat_buffer = [x, y]
                    elif dest not in range(computers):
                        raise ValueError(dest)
                    else:
                        if verbose:
                            print(f'cpu {computer}: sent {x}, {y} to {dest}')
                        cpu_inputs[dest].extend([x, y])
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
            offsets[computer] = offset
            relative_bases[computer] = relative_base
            instructions[computer] = inputs


def part_one():
    return run(source_inputs, 50)
    

def part_two():
    return run(source_inputs, 50, True)


print(part_one())
print(part_two())