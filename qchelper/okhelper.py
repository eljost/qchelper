#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from jinja2 import Template
import numpy as np


def ao_order_from_qcinfo(qcinfo):
    """Get the ordering of the basis functions (AOs) from a QCInfo object.

    Returns a dict containing the atom number as keys. The values correspond
    to lists of the AO types.
    { "0" : ["s", "s", "p", ...],
      "1" : ["s", "s", "p", "s", "p", "d", "d", ...],
      ...
    }
    """
    aos_per_atom = get_aos_per_atom(qcinfo)
    ao_order_dict = dict()
    for atom in aos_per_atom:
        aos = aos_per_atom[atom]
        ao_order_dict[atom] = [ao["type"] for ao in aos]
    return ao_order_dict


def set_mo_symmetries(qcinfo, symmetries):
    for mo, sym in zip(qcinfo.mo_spec, symmetries):
        mo["sym"] = sym


def get_verbose_aos(qcinfo):
    ao_names = {
        "s": ["s", ],
        "p": ["px", "py", "pz"],
        "d": ["dz2", "dxz", "dyz", "dx2-y2", "dxy"],
    }
    verbose_aos = list()
    for ao in qcinfo.ao_spec:
        verbose_aos.extend(ao_names[ao["type"]])
    return verbose_aos


def qcinfo_to_molden(qcinfo, fn):
    """Write information from a QCInfo object to a molden file."""
    with open("/home/carpx/Code/qchelper/qchelper/templates/molden.tpl") as handle:
        tpl = Template(handle.read())
    atoms = [[element, int(float(number)), int(float(Z))]
             for element, number, Z in qcinfo.geo_info]
    geo_spec = qcinfo.geo_spec.astype("float")
    for i, coords in enumerate(geo_spec):
        atoms[i].extend(coords)
    aos_per_atom = get_aos_per_atom(qcinfo)
    mos = qcinfo.mo_spec
    rendered = tpl.render(atoms=atoms, aos_per_atom=aos_per_atom, mos=mos)
    with open(fn, "w") as handle:
        handle.write(rendered)


def get_aos_per_atom(qcinfo):
    """Returns a dict with the atom number as keys and the AOs in a list
    as values."""
    aos_per_atom = OrderedDict()
    for ao in qcinfo.ao_spec:
        aos_per_atom.setdefault(ao["atom"], list()).append(ao)
    return aos_per_atom


def reorder_qcinfo_aos(qcinfo, ao_order_dict):
    """Reorders the AOs in a qcinfo in place."""
    # Number of basis function per AO
    funcs_per_ao = {
        "s": 1,
        "p": 3,
        "d": 5,
        "f": 7,
    }
    aos = qcinfo.ao_spec
    ao_types = [ao["type"] for ao in aos]
    func_nums = [funcs_per_ao[aot] for aot in ao_types]
    offset = 0
    # Contains the offsets of the mo coefficients
    for i, funcn in enumerate(func_nums):
        upper_bound = offset + funcn
        qcinfo.ao_spec[i]["slice"] = (offset, upper_bound)
        offset = upper_bound

    # AO_spec in Basisfukntionen pro center splitten
    aos_per_atom = get_aos_per_atom(qcinfo)

    ordered_ao_spec = list()
    ordered_aos = list()
    for atom in aos_per_atom:
        aos_on_atom = aos_per_atom[atom]

        """Create one dict per atom. Keep the AOs in this dict
        with the corresponding type as key.
        {
            "s": [ao1, ao2, ...],
            "p": [ao3, ...],
            ...
        }"""
        aos_per_type = OrderedDict()
        for ao in aos_on_atom:
            aos_per_type.setdefault(ao["type"], list()).append(ao)

        new_order = ao_order_dict[atom]
        ordered_aos_on_atom = list()
        for ao_type in new_order:
            # Pop an AO of this type from the lists that are stored
            # in the aos_per_type dict.
            ao = aos_per_type[ao_type].pop(0)
            # Save the AO in the new ordered ao_spec
            ordered_ao_spec.append(ao)
            # Expand the stored slice into a list of integers and
            # keep them in the ordered index array.
            ordered_aos_on_atom.extend(list(range(*ao["slice"])))
        ordered_aos.extend(ordered_aos_on_atom)
    qcinfo.ao_spec = ordered_ao_spec
    for mo in qcinfo.mo_spec:
        mo["coeffs"] = mo["coeffs"][ordered_aos]

if __name__ == "__main__":
    import orbkit as ok
    np.set_printoptions(suppress=True)
    fn = "/home/carpx/Code/symmforce/coen/coen3.coenstd.mc_geom.g09.molden"
    #fn = "/home/carpx/Code/symmforce/coen/coen3.coenstd.ordered.mc.molden"
    qci = ok.read.main_read(fn, itype="molden", all_mo=True)
    #qcinfo_to_molden(qci)
    #print(ao_order_from_qcinfo(qci))
    print(get_verbose_aos(qci))
