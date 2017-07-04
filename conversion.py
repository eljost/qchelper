#!/usr/bin/env python3

# Speed of light in m/s
c = 299792458
# Planck constant in J/s
h = 6.626070040e-34
# Electronvol in J
eV = 1.602176565e-19


def invcm2J(invcm):
    return h * c * invcm * 100


def invcm2eV(invcm):
    return invcm2J(invcm) / eV

def au2eV(au):
    return au*27.211396132


if __name__ == "__main__":
    import numpy as np
    invcm = np.array((19496.4,  17163.9,  21976. ,  22727.6,  26192.2,  23612.5,
                      30362.9,  29120.7,  31072.8,  33303.7))
    print(invcm2eV(invcm))
