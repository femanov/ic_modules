# demag/remag path db for injection complex

main_modes = ('e2v4', 'p2v4', 'e2v2', 'p2v2')

mode_colors = {
    'einj': '#f0f0f0',
    'eext': '#f0f0f0',
    'pinj': '#f0f0f0',
    'pext': '#f0f0f0',
    'e2v4': '#55ffff',
    'p2v4': '#ff86ff',
    'e2v2': '#75ff91',
    'p2v2': '#ff6b6b',
}

coefs_set = {
    'd3m4n5': [
        None,
        None,
        None,

        None,
        None,
        None,

        None,
        None,
        [1.0, 1.05, 1.0],

        None,
        None,
        None,

        None,
        None,
        None,
        None,
    ],

    'd5M1t4': [
        None,
        None,
        None,

        None,
        None,
        None,

        None,
        None,
        [1.0, 1.05, 1.0],

        None,
        None,
        None,

        None,
        None,
        None,
        None,
    ],

    'd6M1t4': [
        None,
        None,
        None,

        None,
        None,
        None,

        None,
        None,
        [1.0, 1.05, 1.0],

        None,
        None,
        None,

        None,
        None,
        None,
        None,
    ],
}

path_set = {
    'd3m4n5': [
        ['e2v2', 'p2v2'],
        ['e2v2', 'p2v4'],
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
        ['e2v2', 'p2v4'],
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
        ['e2v2', 'p2v2', 'p2v4'],
        ['e2v2', 'p2v2', 'e2v4'],

        ['p2v2', 'e2v2'],
        ['p2v2', 'p2v4'],
        ['p2v2', 'e2v4'],

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


# None mode neams unknown
def mode_path(mag_name, start_mode, target_mode):
    for x in path_set[mag_name]:
        if x[0] == start_mode and x[-1] == target_mode:
            return x


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
