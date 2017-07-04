#!/usr/bin/env python3

"""This script can be used to create a Jmol-script to render
NTO-molden-files created by ORCA."""

import argparse
from collections import OrderedDict, namedtuple
import os
import re
import sys

from jinja2 import Template
from natsort import natsorted
import numpy as np
import yaml

NTOPair = namedtuple("NTOPair", "state weight from_mo to_mo from_fn to_fn")

TPL= """
{% for molden_fn, nto_pairs in states %}
load {{ molden_fn }} FILTER "nosort"
mo titleformat ""
frank off
set showhydrogens false;

{{ orient }}

function _setModelState() {

    select;
    Spacefill 0.0;

    frank off;
    font frank 16.0 SansSerif Plain;
    select *;
    set fontScaling false;

}

_setModelState;

background white
mo fill
mo cutoff 0.04

mo nomesh
mo COLOR [0,255,0] [255,255,0]
mo resolution 6
{% for nto_pair in nto_pairs %}
mo {{ nto_pair.from_mo }}
write image png "{{ img_base_path}}/{{ nto_pair.from_fn }}"
mo {{ nto_pair.to_mo }}
write image png "{{ img_base_path}}/{{ nto_pair.to_fn }}"
{% endfor %}
{% endfor %}
"""

def get_nto_pairs(molden_fn, uhf=False):
    nto_fn_base = "NTO{}{}_{}{}_{:.2f}.png"
    fn_re = "(.+)\.(s|t)(\d+)(?:\.nto)?\.cut\.molden"

    mobj = re.match(fn_re, molden_fn)
    base_fn, mult, state = mobj.groups()
    with open(molden_fn) as handle:
        text = handle.read()
    occs = [float(occ) for occ
            in re.findall("Occup=\s*([\d\.]+)", text)]
    spins = re.findall("Spin=\s*(\w+)", text)
    assert((len(occs) % 2 == 0) and
           (len(spins) % 2 == 0) and
           (len(occs) == len(spins)))
    ntos_zipped = list(zip(occs, spins))
    nto_total_number = len(ntos_zipped)
    nto_pairs_number = nto_total_number // 2

    if uhf:
        alpha_indices = np.array([(i, nto_pairs_number-i-1)
                                     for i in range(nto_pairs_number//2)]
        )
        beta_indices = alpha_indices + nto_pairs_number
        nto_pair_indices = np.vstack((alpha_indices, beta_indices))
    else:
        nto_pair_indices = np.array([(i, nto_total_number-i-1)
                                     for i in range(nto_total_number // 2)]
        )

    nto_dict = OrderedDict()
    for from_ind, to_ind in nto_pair_indices:
        key = ntos_zipped[from_ind]
        from_occ, from_spin = key
        if from_occ < .1:
            continue
        # Add 1 because JMol MOs start at 1
        nto_dict[key] = (from_ind+1, to_ind+1)

    nto_pairs = list()
    # No symmetry in ORCA, so we always assign irrep A
    irrep = "a"
    for pair, key in enumerate(nto_dict.keys(), 1):
        weight, spin = key
        from_mo, to_mo = nto_dict[key]
        fmt_tpl = lambda ov: (state, irrep, pair, ov, weight)
        nto_occ_fn = nto_fn_base.format(*fmt_tpl("o"))
        nto_virt_fn = nto_fn_base.format(*fmt_tpl("v"))
        nto_pairs.append(NTOPair(
                            state=state,
                            weight=weight,
                            from_mo=from_mo,
                            to_mo=to_mo,
                            from_fn=nto_occ_fn,
                            to_fn=nto_virt_fn
        ))

    return nto_pairs


def states_to_yaml(states):
    states_dict = dict()
    for molden_fn, nto_pairs in states:
        state = int(nto_pairs[0].state)
        states_dict[state] = [[round(ntop.weight, 3), ntop.from_fn, ntop.to_fn]
                              for ntop in nto_pairs]
    return yaml.dump(states_dict)


def get_jmol_nto_script(molden_fns, base_path, img_base_path, orient, uhf):
    full_molden_fns = [os.path.join(base_path, mfn) for mfn in molden_fns]
    states = [(mfn, get_nto_pairs(fmfn, uhf=uhf))
               for mfn, fmfn in zip(molden_fns, full_molden_fns)]
    tpl = Template(TPL)
    rendered = tpl.render(states=states,
                          orient=orient,
                          img_base_path=img_base_path)

    return rendered, states_to_yaml(states)
