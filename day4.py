import aocd

data = aocd.data
data_ = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
cards = data.split('\n')


def load_cards():
    match_by_ids = dict()
    for card in cards:
        card_id, card_data = card.split(': ')
        id_pts = card_id.split(' ')
        id_num = int(id_pts[len(id_pts) - 1].strip())
        winning_numbers, card_numbers = card_data.split(' | ')
        winning_numbers = winning_numbers.split(' ')
        winning_numbers = {int(n.strip()) for n in filter(None, winning_numbers)}

        card_numbers = card_numbers.split(' ')
        card_numbers = {int(n.strip()) for n in filter(None, card_numbers)}

        n_match = len(card_numbers.intersection(winning_numbers))
        match_by_ids[id_num] = n_match
    return match_by_ids


def part_1():
    match_by_ids = load_cards()
    sum = 0
    for n_match in match_by_ids.values():
        if n_match > 0:
            pts = pow(2, n_match - 1)
            sum += pts
    return sum


def part_2():
    match_by_ids = load_cards()
    max_num = len(match_by_ids)
    my_cards = dict(zip(match_by_ids.keys(), [1] * max_num))
    for card_id in range(1, max_num + 1):
        count = my_cards[card_id]
        n_match = match_by_ids[card_id]
        for i in range(1, n_match + 1):
            my_cards[card_id + i] += count
    return sum(my_cards.values())


print(part_2())
