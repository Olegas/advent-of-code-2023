import aocd
from tqdm import tqdm

data = aocd.data
data_ = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
data = data.splitlines()

cave = dict()
for y in range(0, len(data)):
    for x in range(0, len(data[0])):
        p = (x, y)
        s = data[y][x]
        cave[p] = s


def simulate(from_pos, in_direction):
    seen_states = set()
    energized = set()
    beams = [(from_pos, in_direction)]
    while beams:
        beam = beams.pop()
        if beam not in seen_states:
            seen_states.add(beam)
            pos, direction = beam
            x, y = pos
            dx, dy = direction
            if x + dx < 0 or x + dx == len(data[0]):
                continue
            if y + dy < 0 or y + dy == len(data):
                continue
            np = (x + dx, y + dy)
            energized.add(np)
            ns = cave[np]
            if ns == '|':
                if dx != 0:
                    beams.append((np, (0, 1)))
                    beams.append((np, (0, -1)))
                    continue
            elif ns == '-':
                if dy != 0:
                    beams.append((np, (-1, 0)))
                    beams.append((np, (1, 0)))
                    continue
            elif ns == '\\':
                if dx == 0:
                    if dy == 1:
                        direction = (1, 0)
                    else:
                        direction = (-1, 0)
                else:
                    if dx == 1:
                        direction = (0, 1)
                    else:
                        direction = (0, -1)
            elif ns == '/':
                if dx == 0:
                    if dy == 1:
                        direction = (-1, 0)
                    else:
                        direction = (1, 0)
                else:
                    if dx == 1:
                        direction = (0, -1)
                    else:
                        direction = (0, 1)
            else:
                assert ns == '.', f'Must not reach here. {np}, {ns}'

            beams.append((np, direction))
    return len(energized)


def part_1():
    print(simulate((-1, 0), (1, 0)))


def part_2():
    max_v = 0
    left_edge = [((-1, i), (1, 0)) for i in range(0, len(data))]
    for params in left_edge:
        max_v = max(max_v, simulate(*params))
    right_edge = [((len(data[0]), i), (-1, 0)) for i in range(0, len(data))]
    for params in right_edge:
        max_v = max(max_v, simulate(*params))
    top_edge = [((i, -1), (0, 1)) for i in range(0, len(data[0]))]
    for params in top_edge:
        max_v = max(max_v, simulate(*params))
    bottom_edge = [((i, -1), (0, -1)) for i in range(0, len(data[0]))]
    for params in bottom_edge:
        max_v = max(max_v, simulate(*params))
    print(max_v)


part_1()
part_2()
