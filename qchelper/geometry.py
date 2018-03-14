import numpy as np
from pandas import DataFrame

import chemcoord as cc


def get_coords_diffs(coords_list, normalize=False):
    cds = [0, ]
    for i in range(len(coords_list)-1):
        diff = np.linalg.norm(coords_list[i+1]-coords_list[i])
        cds.append(diff)
    cds = np.cumsum(cds)
    if normalize:
        cds /= cds.max()
    return cds


def make_xyz_str(atoms, coords, comment=""):
    assert(len(atoms) == len(coords))

    coord_fmt = "{: 03.8f}"
    line_fmt = "{:>3s} " + " ".join([coord_fmt, ]*3)

    body = [line_fmt.format(a, *xyz)
            for a, xyz
            in zip(atoms, coords)]
    body = "\n".join(body)
 
    return "{}\n{}\n{}".format(len(atoms), comment, body)


def make_trj_str(atoms, coords_list):
    xyz_strings = [make_xyz_str(atoms, coords) for coords in coords_list]
    return "\n".join(xyz_strings)


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

    # Only consider the first four items on a line
    atoms_coords = [line.strip().split()[:4]
                    for line in xyz_str.strip().split("\n")[2:]
    ]
    atoms, coords = zip(*[(a, c) for a, *c in atoms_coords])
    coords = np.array(coords, dtype=np.float)
    return atoms, coords


def parse_xyz_file(xyz_fn):
    with open(xyz_fn) as handle:
        xyz_str = handle.read()

    return parse_xyz_str(xyz_str)


def parse_trj_file(trj_fn):
    with open(trj_fn) as handle:
        trj_str = handle.read()

    return parse_trj_str(trj_str)


def parse_trj_str(trj_str):
    trj_lines = trj_str.strip().split("\n")
    number_of_atoms = int(trj_lines[0].strip())
    xyz_lines = number_of_atoms + 2
    # Split the trj file in evenly sized strings
    xyz_strs = ["\n".join(trj_lines[i:i+xyz_lines])
                for i in range(0, len(trj_lines), xyz_lines)]
    xyzs = [parse_xyz_str(xyz_str) for xyz_str in xyz_strs]

    assert(len(xyzs) == (len(trj_lines) / xyz_lines))
    return xyzs


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
