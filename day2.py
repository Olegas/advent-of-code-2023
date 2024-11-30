import aocd
from aocd import submit
from functools import reduce

# 12, 13, 14
limits = {'red': 12, 'green': 13, 'blue': 14}

data = aocd.data
data_ = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

lines = data.split('\n')
print(lines)


def part_1():
    id_sum = 0
    for line in lines:
        game_id, rounds = line.split(': ')
        game_id = int(game_id.replace('Game ', ''))
        rounds = rounds.split('; ')
        rounds_ok = True
        for item in rounds:
            if not rounds_ok:
                break
            item = item.split(', ')
            ok = True
            for pt in item:
                if not ok:
                    break
                num, kind = pt.split(' ')
                if int(num) > limits[kind]:
                    ok = False
            if not ok:
                rounds_ok = False
        if rounds_ok:
            id_sum += game_id

    submit(id_sum)

def part_2():
    sum = 0
    for line in lines:
        cubes_count = {'red': None, 'green': None, 'blue': None}
        game_id, rounds = line.split(': ')
        game_id = int(game_id.replace('Game ', ''))
        rounds = rounds.split('; ')
        for one_round in rounds:
            cubes = one_round.split(', ')
            for cube in cubes:
                num, kind = cube.split(' ')
                num = int(num)
                cubes_count[kind] = max(cubes_count[kind], num) if cubes_count[kind] is not None else num
        print(cubes_count)
        power = reduce(lambda m, v: m * v, filter(None, cubes_count.values()), 1)
        print(power)
        sum += power
    submit(sum, part='b')

part_2()