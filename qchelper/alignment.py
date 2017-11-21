#!/usr/bin/env python

import chemcoord as cc
import numpy as np

def get_centered_location(cart):
    cartm = cart.sort_index()
    cartm[:, "x":"z"] = cartm[:,"x":"z"] - cartm.topologic_center()
    return cartm.location()

def subalign(structure1, structure2):
    # Unpack the structure tuples into a Cartesian and an index mask.
    cart1, mask1 = structure1
    cart2, mask2 = structure2

    # Create new Cartesians with the substructures.
    sub1 = cc.xyz_functions.Cartesian(cart1[mask1, "atom" : "z"])
    sub2 = cc.xyz_functions.Cartesian(cart2[mask2, "atom" : "z"])

    # Shortcut for get_centered_location.
    gcl = get_centered_location

    # Obtain the rotation matrix U for the two subsystems.
    sub1mloc = gcl(sub1)
    sub2mloc = gcl(sub2)
    U = cc.utilities.kabsch(sub2mloc, sub1mloc)

    # Use the obtained rotation matrix to superimpose cart2
    # on cart1.
    cart1m = cart1.sort_index()
    cart2loc = gcl(cart2)
    cart2m = cart2.sort_index()
    cart2m[:, "x":"z"] = np.dot(cart2loc, U)

    return cart1m, cart2m

if __name__ == "__main__":
    mask1 = [32, 33, 37, 38, 39, 40]
    mask2 = [30, 31, 35, 36, 37, 38]
    fn1 = "xyzs/rubpp.xyz"
    fn2 = "xyzs/ru3bpp.xyz"
    cart1 = cc.xyz_functions.read_xyz(fn1)
    cart2 = cc.xyz_functions.read_xyz(fn2)
    structure1 = (cart1, mask1)
    structure2 = (cart2, mask2)

    cart1m, cart2m = subalign(structure1, structure2)
