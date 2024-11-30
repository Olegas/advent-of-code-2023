import aocd
from tqdm import tqdm

data = aocd.data
data_ = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

lines = data.splitlines()
rocks = dict()
for y in range(0, len(lines)):
    for x in range(0, len(lines[0])):
        p = (x, y)
        s = lines[y][x]
        rocks[p] = s


def vis():
    for y in range(0, len(lines)):
        print('')
        for x in range(0, len(lines[0])):
            p = (x, y)
            s = rocks[p]
            print(s, end='')
    print('')


def run_step_vertical(dy):
    y_range = range(1, len(lines)) if dy == -1 else range(len(lines) - 1, -1, -1)
    for y in y_range:
        for x in range(0, len(lines[0])):
            p = (x, y)
            s = rocks[p]
            if s == 'O':
                ys = y
                while ys > 0 if dy == -1 else ys < len(lines) - 1:
                    p_prev = (x, ys + dy)
                    up = rocks[p_prev]
                    if up == '.':
                        rocks[p_prev] = 'O'
                        rocks[p] = '.'
                        p = p_prev
                        ys += dy
                    else:
                        break


def run_horizontal_step(dx):
    x_range = range(1, len(lines[0])) if dx == -1 else range(len(lines[0]) - 1, -1, -1)
    for x in x_range:
        for y in range(0, len(lines)):
            p = (x, y)
            s = rocks[p]
            if s == 'O':
                xs = x
                while xs > 0 if dx == -1 else xs < len(lines[0]) - 1:
                    p_prev = (xs + dx, y)
                    up = rocks[p_prev]
                    if up == '.':
                        rocks[p_prev] = 'O'
                        rocks[p] = '.'
                        p = p_prev
                        xs += dx
                    else:
                        break


def cycle():
    run_step_vertical(-1)
    run_horizontal_step(-1)
    run_step_vertical(1)
    run_horizontal_step(1)


def calc_load():
    sa = 0
    for y in range(0, len(lines)):
        sl = 0
        for x in range(0, len(lines[0])):
            p = (x, y)
            s = rocks[p]
            if s == 'O':
                sl += 1
        sa += sl * (len(lines) - y)
    return sa


def part_1():
    run_step_vertical(-1)
    print(f'Part 1: {calc_load()}')


def part_2():
    first_seen_on_cycle = dict()
    rocks_on = tuple(sorted(list(p for p, r in rocks.items() if r == 'O')))
    first_seen_on_cycle[rocks_on] = 0
    seen = {rocks_on}
    max_cycle = 1000000000
    for i in tqdm(range(0, max_cycle)):
        cycle()
        rocks_on = tuple(sorted(list(p for p, r in rocks.items() if r == 'O')))
        if rocks_on in seen:
            first_seen_at = first_seen_on_cycle[rocks_on]
            print(f'Pattern repeated at {i} iteration')
            print(f'First seen after {first_seen_at} iterations')
            cycle_length = i - first_seen_at
            print(f'Cycle length {cycle_length}')
            break
        first_seen_on_cycle[rocks_on] = i
        seen.add(rocks_on)

    print(f'Iterations left in cycle {max_cycle - first_seen_at}')
    remainder = (max_cycle - first_seen_at - 1) % cycle_length
    print(f'Remainder {remainder}')
    for i in range(0, remainder):
        cycle()

    print(calc_load())


# part_1()
part_2()
