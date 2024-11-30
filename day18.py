import functools
from collections import defaultdict
from tqdm import tqdm

import aocd

data = aocd.data
data_ = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
data = data.splitlines()

diff = {
    'R': (1, 0),
    'L': (-1, 0),
    'D': (0, 1),
    'U': (0, -1)
}


def parse_part_1(data):
    res = []
    for line in data:
        direction, distance, _ = line.split(' ')
        res.append((direction, int(distance)))
    return res


def parse_part_2(data):
    num_to_dir = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U'
    }
    res = []
    for line in data:
        _, __, color = line.split(' ')
        distance_s = color[2:-2]
        direction = color[-2:-1]
        res.append((num_to_dir[direction], int(distance_s, 16)))

    return res


def optimize(lines_and_dots):
    i = 0
    res = []
    while i < len(lines_and_dots):
        a = lines_and_dots[i]
        if i == len(lines_and_dots) - 1:
            res.append(a)
            break
        b = lines_and_dots[i + 1]
        if len(a) == 1 and len(b) == 1:
            # . .
            res.append(a)
            i += 1
        elif len(a) == 1 and len(b) == 2:
            # . -
            if a[0] == b[0] - 1:
                res.append((a[0], b[1]))
                i += 2
                continue
            res.append(a)
            i += 1
        elif len(a) == 2 and len(b) == 1:
            # - .
            if a[1] + 1 == b[0]:
                res.append((a[0], b[0]))
                i += 2
                continue
            res.append(a)
            i += 1
        else:
            # - -
            res.append(a)
            i += 1
    return tuple(res)


@functools.cache
def line_changes_side(line, y, v_lines):
    x1, x2 = line
    ty = y - 1
    by = y + 1
    left_top_present = any(y1 <= ty <= y2 and x == x1 for y1, y2, x in v_lines)
    left_bottom_present = any(y1 <= by <= y2 and x == x1 for y1, y2, x in v_lines)
    assert left_top_present or left_bottom_present, 'Incorrect line, not left continuation'
    side_left = 1 if left_top_present else 0

    right_top_present = any(y1 <= ty <= y2 and x == x2 for y1, y2, x in v_lines)
    right_bottom_present = any(y1 <= by <= y2 and x == x2 for y1, y2, x in v_lines)
    assert right_top_present or right_bottom_present, 'Incorrect line, no right continuation'
    side_right = 1 if right_top_present else 0

    return side_left != side_right


@functools.cache
def count_area(lines_and_dots, y, v_lines):
    s = 0
    memo = None
    lines_and_dots = optimize(lines_and_dots)
    inside = False
    for i in lines_and_dots:
        if len(i) == 1:
            # dot
            if inside:
                # now outside
                inside = False
                s += i[0] - memo + 1
                memo = None
            else:
                # now inside
                inside = True
                memo = i[0]
        else:
            # line
            will_change = line_changes_side(i, y, v_lines)
            if inside:
                if will_change:
                    # move outside
                    s += i[1] - memo + 1
                    inside = False
                    memo = None
                else:
                    # still inside - move on
                    pass
            else:
                # outside
                if will_change:
                    inside = True
                    memo = i[0]
                else:
                    # outside/line/outside - just add line width
                    s += i[1] - i[0] + 1
    return s


def solve(instructions):
    h_lines = defaultdict(list)
    v_lines = []

    x, y = 0, 0
    for direction, distance in instructions:
        if direction in ('L', 'R'):
            if direction == 'L':
                h_lines[y].append((x - distance, x - 1))
                x = x - distance
            else:
                h_lines[y].append((x + 1, x + distance))
                x = x + distance
        else:
            if direction == 'U':
                v_lines.append((y - distance, y - 1, x))
                y = y - distance
            else:
                v_lines.append((y + 1, y + distance, x))
                y = y + distance

    y_values = h_lines.keys()
    min_y = min(y_values)
    max_y = max(y_values)
    for y1, y2, _ in v_lines:
        min_y = min(min_y, y1, y2)
        max_y = max(max_y, y1, y2)

    v_lines = tuple(v_lines)
    s = 0
    for y in tqdm(range(min_y, max_y + 1)):
        lines = h_lines[y]
        dots = [(x,) for y1, y2, x in v_lines if y1 <= y <= y2]
        lines.extend(dots)
        lines = tuple(sorted(lines))
        s += count_area(lines, y, v_lines)
    return s


print(solve(parse_part_1(data)))
print(solve(parse_part_2(data)))
