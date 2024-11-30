import json

import aocd

data = aocd.data
data_ = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

lines = data.splitlines()
grid = dict()
main_loop = set()
start = None
for y in range(0, len(lines)):
    for x in range(0, len(lines[0])):
        pos = (x, y)
        c = lines[y][x]
        if c == 'S':
            start = pos
        grid[pos] = c


def direction_selector(c: complex) -> int:
    return 0 if c.imag > 0 or c.real > 0 else 1


movements = {
    '|': {
        (0, 1): (0, 1),
        (0, -1): (0, -1)
    },
    '-': {
        (1, 0): (1, 0),
        (-1, 0): (-1, 0)
    },
    'L': {
        (-1, 0): (0, -1),
        (0, 1): (1, 0)
    },
    'F': {
        (0, -1): (1, 0),
        (-1, 0): (0, 1)
    },
    'J': {
        (1, 0): (0, -1),
        (0, 1): (-1, 0)
    },
    '7': {
        (1, 0): (0, 1),
        (0, -1): (-1, 0)
    }
}

grid[start] = '|'
direction = (0, 1)
#grid[start] = '7'
#direction = (1, 0)

pos = start_pos = start
loop_len = 0
while True:
    pipe = grid[pos]
    main_loop.add(pos)
    m = movements[pipe]
    direction = m[direction]
    dx, dy = direction
    x, y = pos
    pos = (x + dx, y + dy)
    loop_len += 1
    if pos == start_pos:
        break

print(f'Part A: {int(loop_len / 2)}')

pos_to_right = {
    '|': {
        (0, 1): [(-1, 0)],
        (0, -1): [(1, 0)]
    },
    '-': {
        (1, 0): [(0, 1)],
        (-1, 0): [(0, -1)]
    },
    'L': {
        (-1, 0): [],
        (0, 1): [(-1, 0), (0, 1)]
    },
    'F': {
        (0, -1): [],
        (-1, 0): [(0, -1), (-1, 0)]
    },
    'J': {
        (1, 0): [(1, 0), (0, 1)],
        (0, 1): []
    },
    '7': {
        (1, 0): [],
        (0, -1): [(1, 0), (0, -1)]
    }
}

around = (-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)


def check_right(cur_dir, cur_pos, seen, limits, all_grid):
    x, y = cur_pos
    c = all_grid[cur_pos]
    deltas = pos_to_right[c][cur_dir]
    for d in deltas:
        dx, dy = d
        np = (x + dx, y + dy)
        if np not in seen and np not in limits:
            wave(np, seen, limits)


def wave(wave_pos, seen, limits):
    to_check = [wave_pos]
    while len(to_check) > 0:
        i = to_check.pop()
        x, y = i
        for a in around:
            dx, dy = a
            np = (x + dx, y + dy)
            if np not in seen and np not in limits:
                if np not in limits:
                    seen.add(np)
                to_check.append(np)


max_x = max(x for x, _ in main_loop)
max_y = max(y for _, y in main_loop)
js_map = dict()
for y in range(0, max_y + 1):
    for x in range(0, max_x + 1):
        p = (x, y)
        if p in main_loop:
            s = grid[p]
        else:
            s = '.'
        js_map[f'{x},{y}'] = s

jd = json.dumps({
    'start_sym': grid[start_pos],
    'start_direction': direction,
    'start': start_pos,
    'map': js_map,
    'max_x': max_x,
    'max_y': max_y,
    'path': [f'{x},{y}' for x, y in main_loop]
})
with open('js.json', mode='wt') as f:
    f.write(jd)
# exit(1)

pos = start_pos
seen = set()
while True:
    check_right(direction, pos, seen, main_loop, grid)
    pipe = grid[pos]
    m = movements[pipe]
    direction = m[direction]
    dx, dy = direction
    x, y = pos
    pos = (x + dx, y + dy)
    loop_len += 1
    if pos == start_pos:
        break

print(f'Part B: {len(seen)}')
