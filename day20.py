import functools
from math import lcm

import itertools
from collections import defaultdict
from tqdm import tqdm

import aocd

data = aocd.data
data_ = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
data__ = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
data = data.splitlines()


def load():
    node_links = {}
    node_types = {}

    for line in data:
        node, links = line.split(' -> ')
        node_type = node[:1]
        node_name = node[1:]
        node_types['broadcaster' if node_type == 'b' else node_name] = node_type
        node_links['broadcaster' if node_type == 'b' else node_name] = links.split(', ')

    return node_types, node_links


def flip_flop(_, signal, state):
    if state is None:
        state = 0
    if signal == 1:
        return state, None
    else:
        state = (state + 1) % 2
        return state, state


def conjunction(from_node, signal, state):
    assert state is not None, 'bad & node state'
    state[from_node] = signal
    is_all_on = all(state.values())
    if is_all_on:
        return state, 0
    return state, 1


def passthrough(from_node, signal, state):
    return state, signal


mtd_map = {
    '%': flip_flop,
    '&': conjunction,
    'b': passthrough,
    None: passthrough
}


def run_cycle(state, node_types, node_links, debug_wire=None):
    count_high = 0
    count_low = 1
    pulses = [('button', 0, 'broadcaster')]
    while pulses:
        pulse = pulses.pop()
        from_node, signal, to_node = pulse
        if debug_wire is not None:
            debug_wire(signal, to_node)
        receiver_type = node_types.get(to_node)
        method = mtd_map[receiver_type]
        new_state, signal = method(from_node, signal, state[to_node])
        state[to_node] = new_state
        if signal is not None:
            next_nodes = node_links.get(to_node, [])
            for next_node in next_nodes:
                if signal == 1:
                    count_high += 1
                else:
                    count_low += 1
                pulse = (to_node, signal, next_node)
                pulses.insert(0, pulse)

    return count_high, count_low


def init_state(node_types, node_links):
    state = {
        'broadcaster': 0
    }
    for from_node, to_nodes in node_links.items():
        for to_node in to_nodes:
            dest_type = node_types.get(to_node)
            if dest_type == '&':
                if state.get(to_node) is None:
                    state[to_node] = dict()
                state[to_node][from_node] = 0
            else:
                state[to_node] = 0
    return state


def part_1(button_press_count):
    node_types, node_links = load()
    state = init_state(node_types, node_links)

    i = 0
    count = [0, 0]
    rem = 0
    while i < button_press_count:
        high, low = run_cycle(state, node_types, node_links)
        count = [count[0] + high, count[1] + low]
        i += 1

        state_is_zero = []
        for n, s in state.items():
            if type(s) == int:
                state_is_zero.append(s == 0)
            elif type(s) == dict:
                state_is_zero.append(all(i == 0 for i in s.values()))
        if all(state_is_zero):
            print(f'Cycle len {i}')
            rem = button_press_count % i
            full_cycles = button_press_count // i
            count = [count[0] * full_cycles, count[1] * full_cycles]
            break

    for i in range(0, rem):
        high, low = run_cycle(node_types, node_links)
        count = [count[0] + high, count[1] + low]

    print(count[0] * count[1])


part_1(1000)


def part_2():
    node_types, node_links = load()
    state = init_state(node_types, node_links)
    rx_parent = [src for src, dst in node_links.items() if 'rx' in dst][0]
    rx_sources = [src for src, dst in node_links.items() if rx_parent in dst]
    cycles = [0]*len(rx_sources)
    print(f'Looking for cycles at nodes {rx_sources}')

    for i in tqdm(itertools.count(start=1)):
        def debug(what, where):
            if what == 1 and where in rx_sources and state[]:
                cycle_slot = rx_sources.index(where)
                val = cycles[cycle_slot]
                if val == 0 and i != 1:
                    cycles[cycle_slot] = i
                    print(f'Cycle for {where} at {i} with')
                    if all(cycles):
                        print(lcm(*cycles))
                        raise StopIteration

        try:
            run_cycle(state, node_types, node_links, debug)
        except StopIteration:
            print('Done')
            break


part_2()
