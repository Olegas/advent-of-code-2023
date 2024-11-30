import functools
import itertools
from collections import defaultdict
from tqdm import tqdm

import aocd

data = aocd.data
data_ = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
data = data.splitlines()

workflows = dict()
items = []

parse_workflows = True
for line in data:
    if line.strip() == '':
        parse_workflows = False
        continue
    if parse_workflows:
        wf_id, rest = line.split('{')
        workflow = []
        rest = rest[:-1]
        rest = rest.split(',')
        for i in rest:
            if ':' in i:
                comp, dst = i.split(':')
                act = '>' if '>' in comp else '<'
                sym, val = comp.split(act)
                workflow.append((sym, act, int(val), dst))
            else:
                workflow.append(i)
        workflows[wf_id] = workflow
    else:
        d = line[1:-1].split(',')
        item = dict()
        for i in d:
            s, v = i.split('=')
            item[s] = int(v)
        items.append(item)

print(workflows)
print(items)


def run_item_to_workflow(item, wf_id, workflows):
    wf = workflows[wf_id]
    for step in wf:
        if step == 'A':
            return True
        elif step == 'R':
            return False
        elif type(step) == str:
            return run_item_to_workflow(item, step, workflows)
        else:
            sym, act, val, dst = step
            item_val = item[sym]
            if act == '>':
                res = item_val > val
            else:
                res = item_val < val
            if res:
                if dst == 'A':
                    return True
                elif dst == 'R':
                    return False
                return run_item_to_workflow(item, dst, workflows)
    assert False, 'Can not reach here'


def part_1():
    s = 0
    for item in items:
        if run_item_to_workflow(item, 'in', workflows):
            for v in item.values():
                s += v
    print(s)


def run_range_to_workflows(rng, workflow_key, workflows):
    syms = 'xmas'
    count = 0

    if workflow_key == 'A':
        return calc_ranges_value(rng)
    elif workflow_key == 'R':
        return 0

    workflow = workflows[workflow_key]
    for step in workflow:
        if type(step) == str:
            return count + run_range_to_workflows(rng, step, workflows)
        else:
            sym, act, val, dst = step
            r_pos = syms.index(sym)
            change_range = rng[r_pos]
            a, b = change_range
            if act == '>':
                change_range = (max(a, val + 1), b)
                rest_range = (a, val)
                accept_range = rng[:r_pos] + (change_range,) + rng[r_pos+1:]
                rng = rng[:r_pos] + (rest_range,) + rng[r_pos+1:]
                count += run_range_to_workflows(accept_range, dst, workflows)
            else:
                change_range = (a, min(b, val - 1))
                rest_range = (val, b)
                accept_range = rng[:r_pos] + (change_range,) + rng[r_pos + 1:]
                rng = rng[:r_pos] + (rest_range,) + rng[r_pos + 1:]
                count += run_range_to_workflows(accept_range, dst, workflows)

    return count


def calc_ranges_value(ranges):
    s = 1
    for a, b in ranges:
        s *= b - a + 1
    return s


def part_2():
    rng = ((1, 4000), (1, 4000), (1, 4000), (1, 4000))
    print(run_range_to_workflows(rng, 'in', workflows))


part_1()
part_2()
