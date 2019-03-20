# demag/remag path db for injection complex

# ic operation modes are here.
# idle - is doing nothing
# None - not in this map. None means that we don't know mode due to any reason
# mode_map = {
#     'idle': 0,
#     'einj': 1,
#     'eext': 2,
#     'pinj': 3,
#     'pext': 4,
#     'e2v4': 5,
#     'p2v4': 6,
#     'e2v2': 7,
#     'p2v2': 8,
#     None  : 0
# }
#
# rev_mode_map = ['idle', 'einj', 'eext', 'pinj', 'pext', 'e2v4', 'p2v4', 'e2v2', 'p2v2']

mode_colors = {
    None  : '#ffffff',
    ''    : '#ffffff',
    'idle': None,
    'einj': '#f0f0f0',
    'eext': '#f0f0f0',
    'pinj': '#f0f0f0',
    'pext': '#f0f0f0',
    'e2v4': '#55ffff',
    'p2v4': '#ff86ff',
    'e2v2': '#75ff91',
    'p2v2': '#ff6b6b',
}

path_set = {
    'd3m4n5': [
        ['e2v2', 'p2v2'],
        ['e2v2', 'e2v4', 'p2v4'],
        ['e2v2', 'p2v4', 'e2v4'],

        ['p2v2', 'e2v2'],
        ['p2v2', 'e2v4', 'p2v4'],
        ['p2v2', 'p2v4', 'e2v4'],

        ['e2v4', 'p2v4'],
        ['e2v4', 'e2v2', 'p2v2'],
        ['e2v4', 'p2v2', 'e2v2'],

        ['p2v4', 'e2v4'],
        ['p2v4', 'e2v2', 'p2v2'],
        ['p2v4', 'p2v2', 'e2v2'],

        [None, 'e2v2', 'p2v2'],
        [None, 'p2v2', 'e2v2'],
        [None, 'e2v4', 'p2v4'],
        [None, 'p2v4', 'e2v4'],
    ],

    'd5M1t4': [
        ['e2v2', 'p2v2'],
        ['e2v2', 'e2v4', 'p2v4'],
        ['e2v2', 'p2v4', 'e2v4'],

        ['p2v2', 'e2v2'],
        ['p2v2', 'e2v4', 'p2v4'],
        ['p2v2', 'p2v4', 'e2v4'],

        ['e2v4', 'p2v4'],
        ['e2v4', 'e2v2', 'p2v2'],
        ['e2v4', 'p2v2', 'e2v2'],

        ['p2v4', 'e2v4'],
        ['p2v4', 'e2v2', 'p2v2'],
        ['p2v4', 'p2v2', 'e2v2'],

        [None, 'e2v2', 'p2v2'],
        [None, 'p2v2', 'e2v2'],
        [None, 'e2v4', 'p2v4'],
        [None, 'p2v4', 'e2v4'],
    ],

    'd6M1t4': [
        ['e2v2', 'p2v2'],
        ['e2v2', 'e2v2', 'p2v4'],
        ['e2v2', 'p2v2', 'e2v4'],

        ['p2v2', 'e2v2'],
        ['p2v2', 'e2v4', 'p2v4'],
        ['p2v2', 'p2v4', 'e2v4'],

        ['e2v4', 'p2v4'],
        ['e2v4', 'e2v2', 'p2v2'],
        ['e2v4', 'p2v2', 'e2v2'],

        ['p2v4', 'e2v4'],
        ['p2v4', 'e2v2', 'p2v2'],
        ['p2v4', 'p2v2', 'e2v2'],

        [None, 'e2v2', 'p2v2'],
        [None, 'p2v2', 'e2v2'],
        [None, 'e2v4', 'p2v4'],
        [None, 'p2v4', 'e2v4'],
    ],
}

def mode_name(id):
    try:
        return rev_mode_map[id]
    except IndexError:
        return None

def mode_id(name):
    if name in mode_map:
        return mode_map[name]
    return -1

# None mode neams unknown
def mode_path(mag_name, start_mode, target_mode):
    for x in path_set[mag_name]:
        if x[0] == start_mode and x[-1] == target_mode:
            return x

def mode_path_num(mag_name, start_mode_num, target_mode_num):

    path = mode_path(mag_name, rev_mode_map[start_mode_num], rev_mode_map[target_mode_num])
    return [mode_map[x] for x in path]


def particles_std(particles):
    if particles in ['e-', 'e']:
        return 'e'
    if particles in ['e+', 'p']:
        return 'p'
    return None


def beam_user_std(user):
    if user in ['v3', 'v4', 'vepp3', 'vepp4']:
        return 'vepp4'
    if user in ['v2', 'bep', 'vepp2k','vepp2000']:
        return 'vepp2k'
    return None


def beam_user_short(user):
    if user in ['v3', 'v4', 'vepp3', 'vepp4']:
        return 'v4'
    if user in ['v2', 'bep', 'vepp2k', 'vepp2000']:
        return 'v2'
    return None


def use_case(particles, beam_user):
    p = particles_std(particles)
    u = beam_user_short(beam_user)
    return p + '2' + u


def mode_num(particles, beam_user):
    return mode_map[use_case(particles, beam_user)]
