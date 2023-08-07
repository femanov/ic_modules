import scipy.constants as const

# IC damping
dr_f0 = 10.94e06  # hz
dr_t0 = 1./dr_f0  # turn time


def i2n_dr(Ibeam):
    """
    converts DR current to particle number (e- or e+)
    :param current: beam current in mA
    :return: N - particles number
    """
    return (Ibeam * dr_t0) / (1000.0 * const.e)


