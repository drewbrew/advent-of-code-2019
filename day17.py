"""day 17"""
import sys
from collections import deque, defaultdict
from itertools import permutations


with open('input17.txt') as infile:
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



def run(inputs, part_two=False, part_two_inputs=None):
    live_display = False
    screen_cleared = False
    offset = 0
    x = 0
    y = 0
    char = ''
    grid = {}
    result = 0
    relative_base = 0
    new_inputs = defaultdict(lambda: 0)
    if part_two:
        part_two_inputs = list(part_two_inputs)
    for index, i in enumerate(inputs):
        new_inputs[index] = i
    inputs = new_inputs
    if part_two:
        inputs[0] = 2
        live_display = part_two_inputs[-2] == ord('y')
        if live_display:
            # clear the screen
            print('\033[2J', end='')
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
            return grid if not part_two else result
        elif next_opcode == 3:
            assert not input2_mode
            if live_display and not screen_cleared:
                print('\033[2J', end='')
                screen_cleared = True
            value = part_two_inputs.pop(0)
            store(inputs, offset, input1_mode, value, relative_base)
            offset += 2
        elif next_opcode == 4:
            assert not input2_mode
            assert not output_mode
            last_char = char
            last_output = retrieve(inputs, offset, input1_mode, relative_base)
            if last_output not in range(256):
                result = last_output
                offset += 2
                continue
            char = chr(last_output)
            if live_display:
                if char == '\n' and char == last_char:
                    # reset position to 0
                    print('\033[0;0H', end='')
                else:
                    print(char, end='')
            if char == '\n':
                x = 0
                y += 1
            else:
                grid[(y, x)] = char
                x += 1
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
    grid = run(source_inputs)
    lineup = sorted(grid.items())
    score = 0
    min_y, min_x = lineup[0][0]
    max_y, max_x = lineup[-1][0]
    assert min_x == 0
    assert min_y == 0
    for y in range(1, max_y):
        for x in range(1, max_x):
            if grid[(y, x)] == '.':
                # open space
                continue
            above = grid[(y - 1, x)]
            left = grid[(y, x - 1)]
            right = grid[(y, x + 1)]
            below = grid[(y + 1, x)]
            if all(i != '.' for i in [above, left, right, below]):
                score += x * y
    display_grid(grid)
    return score


def display_grid(grid):
    max_y, max_x = max(grid.keys())
    for y in range(max_y + 1):
        print('\n', end='')
        for x in range(max_x + 1):
            print(grid[y, x], end='')
    print('\n', end='')


def format_steps(steps):
    output = bytearray()
    for step in steps:
        if isinstance(step, str):
            output.append(ord(step))
        else:
            if step == 10:
                # split into two steps
                # because I'm hard-coding this puzzle,
                # I don't particularly care about trying
                # to solve the generic case
                output += bytearray([ord('6'), ord('4')])
            elif step > 10:
                raise ValueError(step)
            else:
                output.append(ord(str(step)))
    return b','.join(output[i:i + 1] for i in range(len(output)))


def part_two(live_display):
    raw_path = [

        'R', 6, 'L', 8, 'R', 8,  # c
        'R', 6, 'L', 8, 'R', 8,  # c
        'R', 4, 'R', 6, 'R', 6, 'R', 4, 'R', 4,  # b
        'L', 8, 'R', 6, 'L', 10, 'L', 10,  # a

        'R', 4, 'R', 6, 'R', 6, 'R', 4, 'R', 4,  # b
        'L', 8, 'R', 6, 'L', 10, 'L', 10,  # a
        'R', 4, 'R', 6, 'R', 6, 'R', 4, 'R', 4,  # b
        'L', 8, 'R', 6, 'L', 10, 'L', 10,  # a
        'R', 6, 'L', 8, 'R', 8,  # c
        'L', 8, 'R', 6, 'L', 10, 'L', 10,  # a
    ]

    move_a = ['L', 8, 'R', 6, 'L', 10, 'L', 10]
    move_b = ['R', 4, 'R', 6, 'R', 6, 'R', 4, 'R', 4]
    move_c = ['R', 6, 'L', 8, 'R', 8]

    assert (
        move_c + move_c + move_b + move_a +
        move_b + move_a + move_b + move_a +
        move_c + move_a
    ) == raw_path
    main_prog = ['C', 'C', 'B', 'A', 'B', 'A', 'B', 'A', 'C', 'A']
    live_display = ['y' if live_display else 'n']
    inputs = b'\n'.join(
        format_steps(move) for move in [main_prog, move_a, move_b, move_c, live_display]
    ) + b'\n'
    return run(source_inputs, True, inputs)


live_display = len(sys.argv) > 1

print(part_one())
print(part_two(live_display))
