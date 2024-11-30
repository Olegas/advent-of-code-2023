import functools
import aocd

data = aocd.data
data_ = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def match(candidate, pattern):
    assert len(candidate) == len(pattern), f'Lengths mismatch {candidate} vs {pattern}'
    for i, c in enumerate(candidate):
        p = pattern[i]
        if p == '?':
            continue
        if p != c:
            return False
    return True


@functools.cache
def count_variations(groups: tuple[int], pattern: str):
    assert len(groups) != 0
    if len(groups) > 1:
        g, *rest = groups
        space_for_rest = sum(rest) + len(rest) - 1
        space_for_current = len(pattern) - space_for_rest - g
        s = 0
        for i in range(0, space_for_current):
            try_pattern = '.' * i + '#' * g + '.'
            if match(try_pattern, pattern[:len(try_pattern)]):
                s += count_variations(tuple(rest), pattern[len(try_pattern):])
        return s

    else:
        g = groups[0]
        space = len(pattern)
        variations = space - g + 1
        ptrns = ['.' * i + '#' * g + '.' * (space - g - i) for i in range(0, variations)]
        ptrns = filter(lambda p: match(p, pattern), ptrns)
        return len(list(ptrns))


def unfold(pattern, groups):
    p = '?'.join([pattern] * 5)
    g = groups * 5
    return p, g


lines = data.splitlines()
lines = map(lambda l: l.split(' '), lines)
lines = [(p, tuple(map(int, g.split(',')))) for p, g in lines]


def part_1():
    sum = 0
    for pattern, groups in lines:
        c = count_variations(groups, pattern)
        sum += c

    print(sum)


def part_2():
    sum = 0
    for pattern, groups in lines:
        pattern, groups = unfold(pattern, groups)
        c = count_variations(groups, pattern)
        sum += c

    print(sum)


part_1()
part_2()
