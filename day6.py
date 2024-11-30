import aocd
from math import sqrt, ceil, floor

data = aocd.data
data_ = """Time:      7  15   30
Distance:  9  40  200"""
lines = data.split('\n')
_, times_str = lines[0].split(':')
_, distances_str = lines[1].split(':')

# part 1
# times = list(map(int, filter(None, times_str.split(' '))))
# distances = list(map(int, filter(None, distances_str.split(' '))))

# part 2
times = [int(''.join(filter(None, times_str.split(' '))))]
distances = [int(''.join(filter(None, distances_str.split(' '))))]

"""
num_ways_mul = 1
for idx, time in enumerate(times):
    winner_dist = distances[idx]
    num_ways = 0
    for t_hold_btn in tqdm(range(0, time + 1)):
        speed = t_hold_btn
        time_travel = time - t_hold_btn
        my_dist = speed * time_travel
        if my_dist > winner_dist:
            num_ways += 1
    print(num_ways)
    num_ways_mul *= num_ways

print(num_ways_mul)
"""

d = pow(times[0], 2) - 4 * distances[0]
x1 = ceil((times[0] - sqrt(d)) / 2)
x2 = floor((times[0] + sqrt(d)) / 2)
print(x1, x2, abs(x1 - x2) + 1)

"""
t_race
max_dist
x - time
hold

(t_race - x) * x > max_dist
t_race * x - x2 > max_dist
-x2 + t_race * x - max_dist > 0
x2 - t_race * x + max_dist < 0

d = b2 - 4ac
d = (-t_race)2 - 4 * max_dist
x12 = t_race +- sqrt(d) / 2
"""
