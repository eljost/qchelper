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

    xlabel = ("Path length / Å")
    if coordinates is None:
        coordinates = range(0, len(energies))
        xlabel = "Scan step"

    fig, ax = plt.subplots()
    ax.plot(coordinates, energies, marker="o", linestyle="-", ms=4)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("E / eV")
    plt.tight_layout()

    return fig, ax
