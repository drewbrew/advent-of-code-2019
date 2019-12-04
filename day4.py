import re


with open('input4.txt') as infile:
    start, end = [int(i) for i in infile.read().strip().split('-')]


def has_adjacent_char(password, part_two=False):
    pw = str(password)
    assert len(pw) == 6
    if not part_two:
        return len(set(pw)) <= 5 and sum(
            a == b for a, b in zip(pw[:-1], pw[1:])
        ) >= 1
    adjacent_chars = list(
        a for a, b in zip(pw[:-1], pw[1:]) if a == b
    )
    print(pw, adjacent_chars)
    if len(adjacent_chars) == 1:
        return sum(
            a == b and b == c for a, b, c in zip(pw[:-2], pw[1:-1], pw[2:])
        ) == 0
    valid_found = False
    for char in set(adjacent_chars):
        start = pw.index(f'{char}{char}')
        print(char, start)
        if start == 0:
            if pw[2] != char:
                valid_found = True
        elif start == 4:
            if pw[start - 1] != char:
                valid_found = True
        else:
            if pw[start - 1] != char and pw[start + 2] != char:
                valid_found = True
    return valid_found


def always_increasing(password):
    pw = str(password)
    assert len(pw) == 6
    sort = ''.join(sorted(pw))
    return sort == pw


def is_valid(password, part_two=False):
    adjacent = has_adjacent_char(password, part_two)
    increasing = always_increasing(password)
    return adjacent and increasing


def part_one(start, end, part_two=False):
    matching = 0
    for x in range(start, end + 1):
        if is_valid(x, part_two):
            if part_two:
                print(x)
            matching += 1
    return matching


assert is_valid('111111')
assert not is_valid('223450')
assert not is_valid('123456')

print('part 1', part_one(start, end))

assert is_valid('112233', True)
assert not is_valid('123444', True)
assert is_valid('111122', True)

print('part 2', part_one(start, end, True))
