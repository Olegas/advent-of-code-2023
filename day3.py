from collections import defaultdict

import aocd
from itertools import product

data = aocd.data
data_ = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
lines = data.split('\n')


def read_field(lines):
    field = defaultdict(lambda: '.')
    for y in range(0, len(lines)):
        for x in range(0, len(lines[0])):
            field[(x, y)] = lines[y][x]
    return field, len(lines[0]), len(lines)


def is_adjacent_to_symbol(field, pos, match):
    x, y = pos
    look_around = set(product([-1, 0, 1], repeat=2)) - {(0, 0)}
    for dx, dy in look_around:
        p = (x + dx, y + dy)
        sym = field[p]
        if match(sym):
            return p
    return False


def get_numbers_next_to_symbols(field_desc, matcher):
    field, max_x, max_y = field_desc
    is_adjacent = False
    digit_accu = ''
    adj_pos = None
    for y in range(0, max_y):
        if is_adjacent:
            yield int(digit_accu)
            is_adjacent = False
        digit_accu = ''
        for x in range(0, max_x):
            pos = (x, y)
            sym = field[pos]
            if sym.isdigit():
                digit_accu += sym
                adj_pos = is_adjacent_to_symbol(field, pos, matcher)
                if adj_pos is not False:
                    is_adjacent = True
            else:
                if is_adjacent:
                    yield int(digit_accu)
                    is_adjacent = False
                digit_accu = ''
    if is_adjacent and digit_accu:
        yield int(digit_accu)


def part_1():
    field_desc = read_field(lines)
    return sum(get_numbers_next_to_symbols(field_desc, lambda s: not s.isdigit() and s != '.'))


def collect_number(field, pos):
    visited = {pos}
    x, y = pos
    number = field[pos]
    left_x = x - 1
    right_x = x + 1
    while True:
        p = (left_x, y)
        s = field[p]
        if s.isdigit():
            visited.add(p)
            number = s + number
        else:
            break
        left_x -= 1

    while True:
        p = (right_x, y)
        s = field[p]
        if s.isdigit():
            visited.add(p)
            number = number + s
        else:
            break
        right_x += 1

    return int(number), visited


def try_find_number(field, pos):
    numbers_here = []
    visited = set()
    x, y = pos
    look_around = set(product([-1, 0, 1], repeat=2)) - {(0, 0)}
    for dx, dy in look_around:
        p = (x + dx, y + dy)
        if p not in visited:
            visited.add(p)
            s = field[p]
            if s.isdigit():
                number, visited_places = collect_number(field, p)
                numbers_here.append(number)
                visited.update(visited_places)

    return numbers_here


def part_2():
    sum_ratios = 0
    field, max_x, max_y = read_field(lines)
    for y in range(0, max_y):
        for x in range(0, max_x):
            pos = x, y
            sym = field[pos]
            if sym == '*':
                numbers_adjacent = try_find_number(field, pos)
                if len(numbers_adjacent) == 2:
                    a, b = numbers_adjacent
                    sum_ratios += a * b
    return sum_ratios


print(part_1())
print(part_2())
