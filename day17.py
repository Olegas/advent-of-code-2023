import aocd
from dataclasses import dataclass, field
from heapq import heapify, heappop, heappush
from typing import Any

data = aocd.data
data_ = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
data_l = data.splitlines()
data_i = list(map(lambda l: list(map(int, l)), data_l))

left_turn = {
    (1, 0): (0, -1),
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (0, -1): (-1, 0)
}

right_turn = {
    (1, 0): (0, 1),
    (-1, 0): (0, -1),
    (0, 1): (-1, 0),
    (0, -1): (1, 0)
}

moves = {
    (1, 0): '>',
    (-1, 0): '<',
    (0, 1): 'v',
    (0, -1): '^'
}


def do_step(pos, direction):
    x, y = pos
    dx, dy = direction
    nx = x + dx
    ny = y + dy
    if 0 <= nx < len(data_i[0]) and 0 <= ny < len(data_i):
        np = (nx, ny)
        heat_inc = data_i[ny][nx]
        return heat_inc, np


def vis(map_dict, path):
    print(chr(27) + "[2J")
    for y in range(0, len(data_i)):
        if y > 0: print('')
        for x in range(0, len(data_i[0])):
            p = (x, y)
            if p in path:
                print(path[p], end='')
            else:
                print(str(map_dict[y][x]), end='')
    print('')


@dataclass(order=True)
class PathItem:
    heat: int
    pos: Any = field(compare=False)
    steps_this_dir: Any = field(compare=False)
    direction: Any = field(compare=False)
    path: Any = field(compare=False)


def solve(part_a):
    seen_routes = dict()

    def apply_step(item: PathItem, _next_dir, _cur_steps):
        _pos = item.pos
        _direction = item.direction
        _heat = item.heat
        next_step = do_step(_pos, _next_dir)
        if next_step:
            heat_inc, np = next_step
            new_heat = _heat + heat_inc
            global_key = (np, _next_dir, _cur_steps + 1)
            if np in item.path:
                return
            if global_key in seen_routes:
                global_heat = seen_routes[global_key]
                if global_heat > new_heat:
                    seen_routes[global_key] = new_heat
                else:
                    return
            else:
                seen_routes[global_key] = new_heat
            new_path = item.path.copy()
            new_path[np] = moves[_next_dir]
            heappush(steps, PathItem(new_heat, np, _cur_steps + 1, _next_dir, new_path))

    # collected heat, pos, steps this dir, direction, path
    steps = [PathItem(0, (0, 0), 0, (1, 0), {})]
    end_pos = (len(data_i[0]) - 1, len(data_i) - 1)
    heapify(steps)
    while True:
        item = heappop(steps)
        steps_this_dir = item.steps_this_dir
        if part_a:
            if item.pos == end_pos:
                return item.heat
            if steps_this_dir < 3:
                apply_step(item, item.direction, steps_this_dir)

            apply_step(item, left_turn[item.direction], 0)
            apply_step(item, right_turn[item.direction], 0)
        else:
            can_turn_or_stop = steps_this_dir >= 4
            if item.pos == end_pos and can_turn_or_stop:
                return item.heat

            if steps_this_dir < 10:
                apply_step(item, item.direction, steps_this_dir)
            if can_turn_or_stop:
                apply_step(item, left_turn[item.direction], 0)
                apply_step(item, right_turn[item.direction], 0)


print(f'Part A: {solve(True)}')
print(f'Part B: {solve(False)}')
