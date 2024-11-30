import aocd
from tqdm import tqdm

data = aocd.data
data_ = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

lines = data.strip().split(',')


def holiday_hash(string):
    v = 0
    for c in string:
        code = ord(c)
        v += code
        v = v * 17
        v = v % 256
    return v

print(sum(holiday_hash(i) for i in lines))

hmap = list(map(lambda _: [], [None]*256))

for item in lines:
    if '=' in item:
        label, strength = item.split('=')
        strength = int(strength)
        box_index = holiday_hash(label)
        box_contents = hmap[box_index]
        if not box_contents:
            box_contents = [(label, strength)]
            hmap[box_index] = box_contents
        else:
            label_was_found = False
            for idx, old_item in enumerate(box_contents):
                old_label = old_item[0]
                if old_label == label:
                    box_contents[idx] = (label, strength)
                    label_was_found = True
                    break
            if not label_was_found:
                box_contents.append((label, strength))
    elif '-' in item:
        label, strength = item.split('-')
        box_index = holiday_hash(label)
        box_contents = hmap[box_index]
        hmap[box_index] = list(i for i in box_contents if i[0] != label)
    else:
        assert False, 'Must not happen'

ss = 0
for idx, box in enumerate(hmap):
    for idx2, item in enumerate(box):
        ss += (idx + 1) * (idx2 + 1) * item[1]
print(ss)