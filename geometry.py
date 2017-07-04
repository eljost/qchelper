import numpy as np
from pandas import DataFrame

import chemcoord as cc


def parse_xyz_str(xyz_str):
    """Parse a xyz string.

    Paramters
    ---------
    xyz_str : str
        The contents of a .xyz file.

    Returns
    -------
    atoms : list
        List of length N (N = number of atoms) holding the
        element symbols.
    coords: np.array
        An array of shape (N, 3) holding the xyz coordinates.
    """

    atoms_coords = [line.strip().split()
                    for line in xyz_str.strip().split("\n")[2:]
    ]
    atoms, coords = zip(*[(a, c) for a, *c in atoms_coords])
    coords = np.array(coords, dtype=np.float)
    return atoms, coords


def parse_xyz_file(xyz_fn):
    with open(xyz_fn) as handle:
        xyz_str = handle.read()

    return parse_xyz_str(xyz_str)


def interpolate_cartesians(cart1, cart2, steps=10):
    """Interpolate from cart1 to cart2."""
    atoms = cart1.frame.values[:,0]
    cart1a, cart2a = cart1.align(cart2)
    coords1 = cart1a.frame.values[:,1:]
    coords2 = cart2a.frame.values[:,1:]
    diff = coords2-coords1
    diff_per_step = diff/steps
    carts = [cart1a, ]
    for i in range(steps):
        tmp_coords = coords1 + i*diff_per_step
        print(tmp_coords.size)
        print(tmp_coords.shape)
        tmp_values = np.zeros((atoms.size, 4), dtype="object")
        tmp_values[:,0] = atoms
        tmp_values[:,1:] = tmp_coords
        tmp_frame = DataFrame.from_records(tmp_values,
                                        columns=cart1a.columns.values)
        tmp_cart = cc.Cartesian(tmp_frame)
        carts.append(tmp_cart)
    carts.append(cart2a)
    return carts

if __name__ == "__main__":
    start_fn = "/scratch/xyz/start.xyz"
    with open(start_fn) as handle:
        xyz_text = handle.read()
    read_xyz(xyz_text)
