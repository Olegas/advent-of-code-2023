import aocd
import math

data = aocd.data
data_ = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

data_ = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

data = data.splitlines()
movements = data[0]
links_dict = dict()
for line in data[2:]:
    source, links = line.split(' = ')
    links_dict[source] = links[1:-1].split(', ')


def walk(from_node, end_detector):
    i = 0
    node = from_node
    steps = 0
    while True:
        m = movements[i % len(movements)]
        idx = 1 if m == 'R' else 0
        node = links_dict[node][idx]
        i += 1
        steps += 1
        if end_detector(node):
            return steps


def part_1():
    print(walk('AAA', lambda i: i == 'ZZZ'))


def part_2():
    nodes = list(filter(lambda i: i[-1] == 'A', links_dict.keys()))
    steps_to_z = [walk(node, lambda i: i[-1] == 'Z') for node in nodes]
    print(math.lcm(*steps_to_z))


part_1()
part_2()
