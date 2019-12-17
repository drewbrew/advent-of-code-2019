"""Day 16: FFT"""

BASE_PATTERN = [0, 1, 0, -1]


def generate_output_pattern(input_, position):
    output = []
    while len(output) < len(input_) + 1:
        for i in BASE_PATTERN:
            output += [i for _ in range(1, position + 1)]
    del output[0]
    return output[:len(input_)]



def apply_pattern(input_):
    output = []
    for i in range(len(input_)):
        pattern = generate_output_pattern(input_, i + 1)
        output.append(
            abs(sum(x * y for x, y in zip(input_, pattern))) % 10
        )
    assert len(output) == len(input_)
    return output
    


assert apply_pattern([1, 2, 3, 4, 5, 6, 7, 8]) == [4, 8, 2, 2, 6, 1, 5, 8]


def part_one(input_):
    output = input_
    for _ in range(100):
        output = apply_pattern(output)
    return ''.join(str(i) for i in output[:8])


def part_two(input_):
    output = input_ * 10000
    offset = int(''.join(str(i) for i in input_[:7]))

    # make sure the input is only repeated twice
    assert len(output) < 2 * offset - 1

    for _ in range(100):
        checksum = sum(output[offset:])
        new_digits = [0] * offset + [int(str(checksum)[-1])]
        for n in range(offset + 2, len(output) + 1):
            checksum -= output[n - 2]
            new_digits += [int(str(checksum)[-1])]
        output = new_digits
    
    return ''.join(str(i) for i in output[offset:offset + 8])

        
with open('input16.txt') as infile:
    puzzle = [int(i) for i in infile.read().strip()]

print(puzzle)

print(part_one(puzzle))

print('here goes')

print(part_two(puzzle))