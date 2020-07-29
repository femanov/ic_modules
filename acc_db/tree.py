#!/usr/bin/env python3

source = [
    (None, 'a'),
    (None, 'b'),
    (None, 'c'),
    ('a', 'a1'),
    ('a', 'a2'),
    ('a2', 'a21'),
    ('a2', 'a22'),
    ('b', 'b1'),
    ('b1', 'b11'),
    ('b11', 'b111'),
    ('b', 'b2'),
    ('c', 'c1'),
]

source1 = [
    (None, 'a'),
    (None, 'b'),
    ('a', 'a1'),
    ('a', 'a2'),
    ('a2', 'a22'),
    ('b', 'b1'),
    ('a2', 'a21'),
    ('b1', 'b11'),
    (None, 'c'),
    ('b11', 'b111'),
    ('b', 'b2'),
    ('c', 'c1'),
]

source2 = [
    (None, 'b'),
    (None, 'a'),
    ('a', 'a1'),
    ('a', 'a2'),
    ('b', 'b1'),
    ('a2', 'a22'),
    ('a2', 'a21'),
    ('b1', 'b11'),
    (None, 'c'),
    ('b11', 'b111'),
    ('b', 'b2'),
    ('c', 'c1'),
]
expected = {
    'a': {'a1': {}, 'a2': {'a21': {}, 'a22': {}}},
    'b': {'b1': {'b11': {'b111': {}}}, 'b2': {}},
    'c': {'c1': {}},
}


def to_nested_set(src):
    tree = {}
    for x in src:
        if x[0] not in tree:
            tree[x[0]] = {x[1]:{}}
        else:
            tree[x[0]][x[1]] = {}
        tree[x[1]] = tree[x[0]][x[1]]
    return tree[None]


out = to_nested_set(source)

for k in out:
    print(k, out[k])

