import json

import aocd
from itertools import combinations

data = aocd.data
data_ = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

expansion = (1000000-1)
lines = data.splitlines()
galaxies = []
rows = set(range(0, len(lines)))
present_rows = set()
cols = set(range(0, len(lines[0])))
present_cols = set()
for y in range(0, len(lines)):
    for x in range(0, len(lines[0])):
        s = lines[y][x]
        if s == '#':
            pos = (x, y)
            galaxies.append(pos)
            present_cols.add(x)
            present_rows.add(y)

absent_cols = sorted(cols - present_cols)
absent_rows = sorted(rows - present_rows)

while absent_cols:
    i = absent_cols[0]
    absent_cols = [c + expansion for c in absent_cols[1:]]
    galaxies = [(x + expansion, y) if x > i else (x, y) for x, y in galaxies]

while absent_rows:
    i = absent_rows[0]
    absent_rows = [r + expansion for r in absent_rows[1:]]
    galaxies = [(x, y + expansion) if y > i else (x, y) for x, y in galaxies]

sum = 0
for g1, g2 in combinations(galaxies, 2):
    x1, y1 = g1
    x2, y2 = g2
    steps_x = abs(x1 - x2)
    steps_y = abs(y1 - y2)
    sum += steps_x + steps_y

print(sum)



