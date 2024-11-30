import functools
from math import log2
from operator import itemgetter

import aocd
from collections import Counter

data = aocd.data
data_ = """##..####..###
.#..####..#..
#...#..#...##
##.#....#.###
...#.##.#.#..
.###....###..
#.########.##
#..##..##..##
.#.#....#.#.."""

lines = data.splitlines()
patterns = []
pattern = []
for line in lines:
    if not line.strip():
        patterns.append(pattern)
        pattern = []
        continue
    pattern.append(line)
patterns.append(pattern)


@functools.cache
def pattern_to_binary(pattern_str):
    l = len(pattern_str)
    n = 0
    for idx, s in enumerate(pattern_str):
        if s == '#':
            n += pow(2, l - idx - 1)
    return n


@functools.cache
def compare_patterns(a, b, smudge_used):
    if a == b:
        return True, smudge_used
    else:
        if smudge_used:
            return False, smudge_used
        ai = pattern_to_binary(a)
        bi = pattern_to_binary(b)
        diff = ai ^ bi
        diff_pos = log2(diff)
        is_single_bit = diff_pos % 1 == 0.0
        if is_single_bit:
            return True, True
        else:
            return False, smudge_used


def transpose_pattern(pattern):
    new_pattern = []
    for i in range(0, len(pattern[0])):
        new_line = ''
        for line in pattern:
            new_line += line[i]
        new_pattern.append(new_line)
    return new_pattern


def find_vertical_mirrors(pattern, smudge_used_initial):
    transposed = transpose_pattern(pattern)
    return find_horizontal_mirrors(transposed, smudge_used_initial)


def find_horizontal_mirrors(pattern, smudge_used_initial):
    pattern_len = len(pattern)
    for idx, line in enumerate(pattern):
        if idx <= pattern_len - 2:
            is_equal, smudge_used = compare_patterns(line, pattern[idx + 1], smudge_used=smudge_used_initial)
            if is_equal:
                smudge_used = smudge_used_initial
                left_index = idx
                shift = 1
                search_from = left_index
                while True:
                    a = pattern[search_from + shift]
                    b = pattern[search_from]
                    is_equal, smudge_used = compare_patterns(a, b, smudge_used)
                    if is_equal:
                        if search_from == 0 or search_from + shift == len(pattern) - 1:
                            if smudge_used:
                                return left_index + 1
                            else:
                                break
                        search_from -= 1
                        shift += 2
                    else:
                        break

    return 0


def part_1():
    s = 0
    for pattern in patterns:
        v = find_vertical_mirrors(pattern, True)
        h = find_horizontal_mirrors(pattern, True)
        assert not v or not h, f'Both kind of mirrors in pattern: {pattern}'
        assert v or h, f'None of mirrors found: {pattern}'

        s += v + 100 * h
    return s


def part_2():
    s = 0
    for pattern in patterns:
        v = find_vertical_mirrors(pattern, False)
        h = find_horizontal_mirrors(pattern, False)
        assert not v or not h, f'Both kind of mirrors in pattern: {pattern}'
        assert v or h, f'None of mirrors found: {pattern}'

        s += v + 100 * h
    return s


print(part_1())
print(part_2())
