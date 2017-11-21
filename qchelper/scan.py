#!/usr/bin/env python3

import matplotlib.pyplot as plt

def plot_scan(energies, coordinates=None):
    """2D plot of a scan.

    Parameters
    ----------
    energies : iterable
               (1D/2D) holding the energies for every geometry of the scan.
    coordinates : iterable, optional
                  The scan coordinate for every geometry. If not provied the
                  steps will be numbered automatically starting from 1.
    """

    if not coordinates:
        coordinates = range(0, len(energies))

    fig, ax = plt.subplots()
    plt.tight_layout()
    ax.plot(coordinates, energies, marker="o", linestyle="-")
    ax.set_xlabel("Scan step")
    ax.set_ylabel("E / eV")
    plt.show()
