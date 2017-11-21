#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def comp_coeffs(mo1, mo2):
    """Calculate the difference between two MO-coefficients-arrays while
    considering a possible phase switch.
    Returns the difference between the arrays mo1 and mo2.
    """
    diff = mo1 - mo2
    diff_norm = np.linalg.norm(diff)
    # Check for phase flip
    diff_flip = mo1 + mo2
    diff_flip_norm = np.linalg.norm(diff_flip)
    if diff_flip_norm < diff_norm:
        # Phase flipped
        return diff_flip
    else:
        return diff


def get_degenerate_indices(values, thresh=1e-6):
    """Returns a list of sets containing the indices of (nearly) degenerate
    values in the argument iterable."""
    diffs = np.abs(values[:-1] - values[1:])
    index_pairs = [set((i, i+1)) for i, d in enumerate(diffs) if d < thresh]

    if not index_pairs:
        return index_pairs

    index_sets = [index_pairs.pop(0), ]
    for pair in index_pairs:
        intersection = index_sets[-1] & pair
        if intersection:
            index_sets[-1] |= pair
        else:
            index_sets.append(pair)
    return index_sets
    
    """ Also include the non degenerate values as tuples of length 1
    i = 0
    indices = list()
    for d in diffs:
        if d < thresh:
            indices.append((i, i+1))
        elif  not (i in indices[-1]):
            indices.append((i, ))
        i += 1
    return indices
    """
    # Join tuples if they contain the same element, e.g. there is more than a double
    # degeneracy, e.g. [(1, 2), (3, 4), (4, 5)]. Here there would be a threefold de-
    # generacy, but this is currently not handled.


def compare_mos(mos1, mos2, check_neighbours=0):
    """Accepts two iterables containing iterables with mo ceofficents. For
    every MO in mos1 the functions looks for the most similar MO in mos2. This
    is done by comparing the norm of the difference vector of the two MO
    coefficient vectors.
    Returns a list of tuples, where the tuple contains the index of the MO in
    mos1, the index of the most similar MO in mo2 and the norm of the
    difference vector of the two MOs.
    """
    similar_mos = list()
    already_matched = list()
    for i, mo1 in enumerate(mos1):
        # Compare all mos
        if check_neighbours is 0:
            lower_bound = 0
            upper_bound = None
        else:
            lower_bound = max(0, i-check_neighbours)
            upper_bound = min(len(mos2), i+check_neighbours)
        mos2_slice = mos2[lower_bound:upper_bound]
        diffs = [np.linalg.norm(comp_coeffs(mo1, mo2)) for mo2
                 in mos2_slice]
        norms = [np.linalg.norm(d) for d in diffs]
        norms = np.array(norms)

        """Assure that we match every MO in mos2 only once! The indices
        of the MOs already matched are kept in the list 'already_matched'.

        Before a match is confirmed it is checked, that the matched index
        isn't already in the 'already matched' array. If it's the case
        the norm of the corresponding index is set to positive infinity
        and the search for the then smallest norm is continued."""

        # Create a copy so we don't modify the original array
        modifiable_norms = np.copy(norms)
        # Continue the search until a minimum_index is found
        while True:
            minimum_index = np.argmin(modifiable_norms)
            if minimum_index in already_matched:
                # Set index to positive infinity so we don't find it again
                modifiable_norms[minimum_index] = np.inf
            else:
                already_matched.append(minimum_index)
                break
        similar_mos.append((i,
                            lower_bound+minimum_index,
                            modifiable_norms.min()))
    return similar_mos

if __name__ == "__main__":
    import orbkit as ok
    print("G09")
    fn = "/home/carpx/Code/symmforce/coen/coen3.coenstd.mc_geom.g09.molden"
    qci = ok.read.main_read(fn, itype="molden", all_mo=True)
    ens = [mo["energy"] for mo in qci.mo_spec]
    ens = np.array(ens)
    degens = get_degenerate_indices(ens)
    for d in degens:
        arr = np.array(tuple(d))
        print(arr+1)
    print("molcas")
    fn = "/home/carpx/Code/symmforce/coen/coen3.coenstd.ordered.mc.molden"
    ens = [mo["energy"] for mo in qci.mo_spec]
    ens = np.array(ens)
    degens = get_degenerate_indices(ens)
    for d in degens:
        arr = np.array(tuple(d))
        print(arr+1)
