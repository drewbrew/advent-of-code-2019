"""day 17"""
import sys
from collections import deque, defaultdict
from itertools import permutations


with open('input19.txt') as infile:
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



def run(inputs, x, y, part_two=False, part_two_inputs=None):
    result = -1
    offset = 0
    relative_base = 0
    new_inputs = defaultdict(lambda: 0)
    if part_two:
        part_two_inputs = list(part_two_inputs)
    for index, i in enumerate(inputs):
        new_inputs[index] = i
    inputs = new_inputs
    if part_two:
        inputs[0] = 2
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
            return result
        elif next_opcode == 3:
            assert not input2_mode
            if y is not None:
                value = y
                y = None
            else:
                value = x
            store(inputs, offset, input1_mode, value, relative_base)
            offset += 2
        elif next_opcode == 4:
            assert not input2_mode
            assert not output_mode
            last_output = retrieve(inputs, offset, input1_mode, relative_base)
            result = last_output
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
    grid = build_grid()
    display_grid(grid)
    return sum(grid.values())


def build_grid(size=50):
    grid = {}
    for y in range(size):
        for x in range(size):
            active = run(source_inputs, x=x, y=y)
            grid[(y, x)] = active
    return grid


def result_found(grid, x, size=100):
    right_column = sorted(
        y for (y, dx), value in grid.items()
        if x == dx and value
    )
    if len(right_column) < 100 or x < 100:
        return False
    y0 = right_column[0]
    y1 = right_column[0] + 99
    x0 = x - 99

    if all(grid.get(pos) for pos in [
        (y0, x0), (y0, x), (y1, x), (y1, x0)
    ]):
        return y0, x0
    

def part_two():
    # start with a 100x100 grid
    grid = build_grid(100)
    x = 99
    found = False
    while not found:
        right_column = sorted(
            y for (y, dx), value in grid.items()
            if x == dx and value
        )
        x += 1
        min_y, max_y = right_column[0] - 2, right_column[-1] + 2
        for y in range(min_y, max_y):
            value = run(source_inputs, x, y)
            grid[(y, x)] = value
        found = result_found(grid, x)
    y, x = found
    print(x, y)
    # not sure why but things are transposed.
    return y * 10000 + x
        


def display_grid(grid, x_offset=0, y_offset=0):
    max_y, max_x = max(grid.keys())
    for y in range(y_offset, max_y + 1):
        print('\n', end='')
        for x in range(x_offset, max_x + 1):
            print(grid.get((y, x), 0), end='')
    print('\n', end='')


def format_steps(steps):
    output = bytearray()
    for step in steps:
        if isinstance(step, str):
            output.append(ord(step))
        else:
            while step >= 10:
                output.append(ord('9'))
                step -= 9
            output.append(ord(str(step)))
    return b','.join(output[i:i + 1] for i in range(len(output)))


live_display = len(sys.argv) > 1

print(part_one())
print(part_two())