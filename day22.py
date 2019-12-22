from collections import deque

from lcgrandom import LcgRandom


def cards(length=10007):
    return deque(range(length))


# seq 1
def reverse_deck(cards):
    result = deque(reversed(cards))
    return result


# seq 2
def cut(cards, depth):
    cards.rotate(0 - depth)
    return cards

# seq 3
def deal(cards, increment):
    new_stack = [None] * len(cards)
    stack = list(cards)
    for index, i in enumerate(stack):
        other_i = (index * increment) % len(new_stack)
        new_stack[other_i] = i
    return deque(new_stack)


def p2_reverse(position, num_cards):
    return num_cards - position - 1


def p2_cut(position, num_cards, depth):
    return (position - depth) % num_cards


def p2_deal(position, num_cards, increment):
    return (position * increment) % num_cards


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)


def p2_parse_input(lines, num_cards, iterations, target):
    assert iterations > 10000
    states = [0]
    pos = 0
    # go through 10 iterations of shuffling to get our PRNG state
    for _ in range(10):
        for line in lines:
            line = line.strip()
            if line.startswith('deal with increment'):
                value = int(line.split()[-1])
                pos = p2_deal(pos, num_cards, value)
            elif line.startswith('cut '):
                value = int(line[4:])
                pos = p2_cut(pos, num_cards, value)
            elif line == 'deal into new stack':
                pos = p2_reverse(pos, num_cards)
            else:
                raise ValueError(line)
        states.append(pos)
    # now crack our PRNG
    modulus, multiplier, increment = crack_unknown_multiplier(states, num_cards)
    # check our assumption
    assert modulus == num_cards
    # so the fast skipping gives us:
    rng = LcgRandom(multiplier, increment, modulus, target)
    rng.skip(num_cards - iterations - 1)
    return rng.get_state()


def parse_input(lines, num_cards=10007, iterations=1):

    deck = cards(num_cards)
    for _ in range(iterations):
        for line in lines:
            line = line.strip()
            if line.startswith('deal with increment'):
                value = int(line.split(' ')[-1])
                deck = deal(deck, value)
            elif line.startswith('cut '):
                value = int(line[4:])
                deck = cut(deck, value)
            elif line == 'deal into new stack':
                deck = reverse_deck(deck)
            else:
                raise ValueError(line)
    return deck


def part_one(lines):
    deck = parse_input(lines)
    return deck.index(2019)


def part_two(lines, cards=119315717514047, iterations=101741582076661):
    deck = parse_input(lines, cards, iterations)
    return deck.index(2020)


with open('input22.txt') as infile:
    lines = [i for i in infile]

# a whole boatload of tests because I'm not at all confident in this

assert reverse_deck(deque(range(10))) == deque(range(9, -1, -1)), reverse_deck(list(range(10)))

assert deal(deque(range(10)), 3) == deque([0, 7, 4, 1, 8, 5, 2, 9, 6, 3])

assert cut(deque(range(10)), 3) == deque([3, 4, 5, 6, 7, 8, 9, 0, 1, 2]), cut(deque(range(10)), 3)

assert reverse_deck(reverse_deck(deal(deque(range(10)), 7))) == deque([
    0, 3, 6, 9, 2, 5, 8, 1, 4, 7
])

deck = deque(range(10))
deck = cut(deck, 6)
deck = deal(deck, 7)
deck = reverse_deck(deck)
assert list(deck) == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6], deck

assert cut(deal(deal(deque(range(10)), 9), 7), -2) == deque([
    6, 3, 0, 7, 4, 1, 8, 5, 2, 9,
])

test_deck = parse_input("""deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""".split('\n'), 10)
assert list(test_deck) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6], test_deck

assert p2_reverse(0, 11) == 10
assert p2_cut(10, 11, -2) == 1
assert p2_deal(1, 11, 7) == 7
assert p2_cut(7, 11, 8) == 10
assert p2_cut(10, 11, -4) == 3
assert p2_deal(3, 11, 7) == 10
assert p2_cut(10, 11, 3) == 7
assert p2_deal(7, 11, 9) == 8
assert p2_deal(8, 11, 3) == 2
assert p2_cut(2, 11, -1) == 3

assert p2_reverse(1, 11) == 9
assert p2_cut(9, 11, -2) == 0
assert p2_deal(0, 11, 7) == 0
assert p2_cut(0, 11, 8) == 3
assert p2_cut(3, 11, -4) == 7
assert p2_deal(7, 11, 7) == 5
assert p2_cut(5, 11, 3) == 2
assert p2_deal(2, 11, 9) == 7
assert p2_deal(7, 11, 3) == 10
assert p2_cut(10, 11, -1) == 0

test_deck = parse_input(["""cut -4"""], 10)
assert list(test_deck) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]

# and now the real thing
print(part_one(lines))
print(p2_parse_input(lines, num_cards=119315717514047, iterations=101741582076661, target=2020))