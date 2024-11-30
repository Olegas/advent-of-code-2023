from functools import reduce
from operator import add

import aocd

data = aocd.data
data_ = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

lines = [list(map(int, line.split(' '))) for line in data.splitlines()]
zs = {0}


def extrapolate(sequence):
    next = [None] * (len(sequence) - 1)
    for i in range(0, len(sequence) - 1):
        next[i] = sequence[i + 1] - sequence[i]
    s = set(next)
    if s == zs:
        return sequence[-1]
    return sequence[-1] + extrapolate(next)


def extrapolate_tail(sequence):
    next = [None] * (len(sequence) - 1)
    for i in range(0, len(sequence) - 1):
        next[i] = sequence[i + 1] - sequence[i]
    s = set(next)
    if s == zs:
        return sequence[0]
    return sequence[0] - extrapolate_tail(next)


e = [extrapolate(line) for line in lines]
print(reduce(add, e))

e = [extrapolate_tail(line) for line in lines]
print(reduce(add, e))
