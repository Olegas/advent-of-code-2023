from collections import Counter
from operator import itemgetter

import aocd


def get_hand_strength(hand_with_bid):
    hand, bid = hand_with_bid
    cards_count = Counter(hand)
    most_common = cards_count.most_common(3)
    if len(most_common) == 1:
        # Five of a kind
        return hand, bid, -1
    else:
        a, b, *_ = most_common
        _, na = a
        if na == 4:
            # Four of a kind
            return hand, bid, -2
        else:
            _, nb = b
            if na == 3 and nb == 2:
                # Full hours
                return hand, bid, -3
            if na == 3 and nb == 1:
                # Three of a kind
                return hand, bid, -4
            if na == 2 and nb == 2:
                # Two pair
                return hand, bid, -5
            if na == 2 and nb == 1:
                # One pair
                return hand, bid, -6
            if na == 1:
                # High card
                return hand, bid, -7
    assert False, 'Can not reach here'


def get_hand_strength_2(hand_with_bid):
    hand, bid = hand_with_bid
    cards_count = Counter(hand)
    joker_count = cards_count['J']
    if joker_count == 5:
        # Five of a kind
        return hand, bid, -1
    del cards_count['J']
    most_common = cards_count.most_common(3)
    if len(most_common) == 1:
        # Five of a kind
        return hand, bid, -1
    else:
        a, b, *_ = most_common
        _, na = a
        _, nb = b

        if joker_count > 0:
            if na + joker_count == 4:
                # Four of a kind
                return hand, bid, -2
            if na == 2:
                if joker_count == 1:
                    if nb == 1:
                        # Three of a kind
                        return hand, bid, -4
                    else:
                        # Full house
                        return hand, bid, -3
                assert False, "Can't reach here"
            if na == 1:
                if joker_count == 1:
                    # One pair
                    return hand, bid, -6
                elif joker_count == 2:
                    # Three of a kind
                    return hand, bid, -4
                assert False, "Can't reach here"
            assert False, "Can't reach here"

        if na == 4:
            # Four of a kind
            return hand, bid, -2
        else:
            _, nb = b
            if na == 3 and nb == 2:
                # Full house
                return hand, bid, -3
            if na == 3 and nb == 1:
                # Three of a kind
                return hand, bid, -4
            if na == 2 and nb == 2:
                # Two pair
                return hand, bid, -5
            if na == 2 and nb == 1:
                # One pair
                return hand, bid, -6
            if na == 1:
                # High card
                return hand, bid, -7
    assert False, 'Can not reach here'


cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
cards_pt_2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']


def get_cards_weight(hand_with_bid_and_strength):
    hand, bid, strength = hand_with_bid_and_strength
    hand_indexes = [strength, list(map(lambda i: -cards.index(i), hand))]
    return hand, bid, strength, hand_indexes


def get_cards_weight_2(hand_with_bid_and_strength):
    hand, bid, strength = hand_with_bid_and_strength
    hand_indexes = [strength, list(map(lambda i: -cards_pt_2.index(i), hand))]
    return hand, bid, strength, hand_indexes


data = aocd.data
data_ = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def part_1():
    lines = data.split('\n')
    hands = map(lambda i: i.split(' '), lines)
    with_strength = map(get_hand_strength, hands)
    with_card_weight = map(get_cards_weight, with_strength)
    all_sorted = sorted(with_card_weight, key=itemgetter(3))
    print(all_sorted)
    sum = 0
    for rank, i in enumerate(all_sorted):
        hand, bid, _, _ = i
        sum += int(bid) * (rank + 1)
    print(sum)


def part_2():
    lines = data.split('\n')
    hands = map(lambda i: i.split(' '), lines)
    with_card_weight = list(map(get_cards_weight_2, map(get_hand_strength_2, hands)))
    for k, _, s, _ in with_card_weight:
        if 'J' in k:
            print(k, s)
    all_sorted = sorted(with_card_weight, key=itemgetter(3))
    print(all_sorted)
    sum = 0
    for rank, i in enumerate(all_sorted):
        hand, bid, _, _ = i
        sum += int(bid) * (rank + 1)
    print(sum)


part_2()
