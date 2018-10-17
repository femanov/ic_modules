import numpy as np

# Sukhanov's coefficients deffinitions
p0_a = np.array([-4.202, -8.528, 32.696, -11.625])
ku_a = np.array([6.000,  5.900,  5.984,   5.924])
zp_a = np.array([1.435,  1.764,  3.859,   1.747])
zl_a = np.array([3.142,  3.082,  2.573,   3.042])
rs_a = np.array([0.025,  0.025,  0.500,   0.080])
b_a = np.array([0.674,  0.810,  0.670,   0.696])
g_a = np.array([0.424,  0.376,  0.406,   0.403])
zp2_a = np.power(zp_a, 2)
rs2_a = np.power(rs_a, 2)


def u2phase(k, u_in):
    p0, ku, zp, zl, rs, b, g, zp2, rs2 = p0_a[k], ku_a[k], zp_a[k], zl_a[k], rs_a[k], b_a[k], g_a[k], zp2_a[k], rs2_a[k]

    if u_in < 0.0:
        u = 0.0
    else:
        u = u_in

    zu  = b * np.power(u * ku, g) - zl
    zu2 = zu ** 2

    phase = np.arctan(-2. * zp * (zu2 + zu * zp + rs2) / (zu2 * zp2 + rs2 * (zp2 - 1.) - zu2 - 2. * zu * zp - zp2))

    zu = rs * (zp2 - 1.)
    zu = (zp - np.sqrt(zp2 * zp2 - zu * zu)) / ((zp2 - 1.) * b) + zl/b
    zu = np.power(zu, 1. / g)
    if u * ku > zu:
        phase += np.pi

    phase = phase * 180. / np.pi - p0
    return phase


def phase2u(k, phase_in):
    p0, ku, zp, zl, rs, b, g, zp2, rs2 = p0_a[k], ku_a[k], zp_a[k], zl_a[k], rs_a[k], b_a[k], g_a[k], zp2_a[k], rs2_a[k]

    if phase_in < 0.:
        phase = 0.
    else:
        phase = phase_in

    phase += p0
    a  = 1.0 - zp2
    a2 = a * a
    if phase > 89.9 and phase < 90.1:
        x = -(zp - np.sqrt(zp2 * zp2 - rs2 * a2)) / a
    else:
        T = np.tan(phase * np.pi / 180.)
        x = np.sqrt((zp2 * zp2 - rs2 * a2) * T * T + 4. * rs2 * zp * a * T + zp2 * (zp2 - 4. * rs2))
        if phase < 90.:
            x = T * zp - zp2 - x
        else:
            x = T * zp - zp2 + x
        x /= 2. * zp - a * T
    x = np.power((x + zl) / b, 1. / g) / ku

    return x