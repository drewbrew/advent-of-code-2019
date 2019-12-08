from collections import Counter

TEST_INPUT = '123456789012'

TEST_WIDTH = 3
TEST_HEIGHT = 2

PART_TWO_TEST_INPUT = '0222112222120000'
PART_TWO_TEST_WIDTH = 2
PART_TWO_TEST_HEIGHT = 2


def parse_image(image, width, height):
    layer_size = width * height
    layers = [image[i:i + layer_size] for i in range(0, len(image), layer_size)]
    result = []
    for layer in layers:
        raw_rows = [layer[i: i + width] for i in range(0, len(layer), width)]

        rows = [
            [int(i) for i in row]
            for row in raw_rows
        ]
        assert len(rows) == height, rows
        result.append(rows)
    return result


def part_one(parsed_image):
    best_layer = {}
    for layer in parsed_image:
        flattened = Counter(sum(layer, []))
        if not best_layer:
            best_layer = flattened
        else:
            if best_layer[0] > flattened[0]:
                best_layer = flattened
    return best_layer[1] * best_layer[2]


def part_two(layers, width, height):
    final_img = [[2] * width for dummy in range(height)]
    for layer in reversed(layers):
        for y, row in enumerate(layer):
            for x, pixel in enumerate(row):
                if pixel == 2:  # transparent
                    continue
                final_img[y][x] = pixel
    return final_img


def display_image(image):
    for row in image:
        print(
            ''.join(' ' if char == 0 else '#' for char in row)
        )

test_image = parse_image(TEST_INPUT, TEST_WIDTH, TEST_HEIGHT)
assert test_image == [
    [
        [1, 2, 3], [4, 5, 6],
    ],
    [
        [7, 8, 9], [0, 1, 2],
    ],
], test_image
test_result = part_one(test_image)
assert test_result == 1, test_result

with open('input8.txt') as infile:
    img = parse_image(infile.read(), 25, 6)

print(part_one(img))

test_result = part_two(
    parse_image(
        PART_TWO_TEST_INPUT, PART_TWO_TEST_WIDTH, PART_TWO_TEST_HEIGHT,
    ),
    PART_TWO_TEST_WIDTH,
    PART_TWO_TEST_HEIGHT,
)

assert test_result == [[0, 1], [1, 0]], test_result

result = part_two(img, 25, 6)
display_image(result)