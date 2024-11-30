import aocd
from tqdm import tqdm

data = aocd.data
data_ = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

lines = data.split('\n')
seeds = list(map(int, lines[0].replace('seeds: ', '').split(' ')))

map_seq = []

maps = dict()
map_mode = False
current_map = None
for line in lines[2:]:
    if 'map' in line:
        map_name, _ = line.split(' ')
        map_seq.append(map_name)
        current_map = maps[map_name] = []
    elif line == '':
        pass
    else:
        current_map.append(tuple(map(int, line.split(' '))))


def get_loc(seed):
    v = seed
    for map_name in map_seq:
        for mapping in maps[map_name]:
            dst_start, src_start, length = mapping
            if src_start <= v < src_start + length:
                v = dst_start + (v - src_start)
                break
    return v


reversed_maps = list(reversed(map_seq))


def seed_by_loc(loc):
    v = loc
    for map_name in reversed_maps:
        for mapping in maps[map_name]:
            dst_start, src_start, length = mapping
            if dst_start <= v < dst_start + length:
                v = src_start + (v - dst_start)
                break
    return v


def part_1():
    locs = []
    for seed in seeds:
        locs.append(get_loc(seed))

    print(locs)
    # submit(min(locs))


def part_2():
    seed_ranges = list(zip(seeds[::2], seeds[1::2]))
    max_item = max(start + length - 1 for start, length in seed_ranges)
    for i in tqdm(range(0, max_item)):
        seed = seed_by_loc(i)
        for start, length in seed_ranges:
            if start <= seed < start + length:
                print(i)
                return


part_1()
part_2()
