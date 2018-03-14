import re
import textwrap

import pyparsing as pp


def get_occupations(text):
    occup_re = "\s*Occup=\s*([-\d\.].+)"
    occups = [float(mo.strip()) for mo in re.findall(occup_re, text)]
    return occups


def get_symmetries(text):
    sym_re = "\s*Sym=\s*(.+)"
    syms = [mo.strip() for mo in re.findall(sym_re, text)]
    # Insert a space after the MO number
    # 40a' will become 40 a'
    syms = [re.sub("(\d+)", r"\1 ", mo) for mo in syms]
    return syms


def get_energies(text):
    en_re = "\s*Ene=\s*(.+)"
    ens = [float(mo.strip()) for mo in re.findall(en_re, text)]
    return ens


def get_jmol_ordering(text):
    ens = get_energies(text)
    syms = get_symmetries(text)
    occups = get_occupations(text)
    zipped = zip(ens, syms, occups)
    sorted_by_energy = sorted(zipped, key=lambda mo: mo[0])
    with_index = [(i+1, en, sym, occ)
                  for i, (en, sym, occ) in enumerate(sorted_by_energy)]
    return with_index


def get_jmol_active_space(text):
    with_index = get_jmol_ordering(text)
    active_space = [mo for mo in with_index
                    if (mo[1] == 0.0)]
    return active_space


def cut_molden(text, indices):
    """Used to shrink a NTO-.molden-file from ORCA."""
    # Split at [MO]
    header, mos = re.split("\[MO\]", text)
    # Never matches the last MO
    # This is actually a pretty bad hack ;(
    mos = re.findall("(Sym=.+?)(?=Sym)", text, re.DOTALL)

    mos_slice = [mos[index].strip() for index in indices]

    # Rename the orbitals, because ORCA uses '1a' for all MOs
    occ_mos = [re.sub("(Sym=\s*)(\d+)", "Sym= {}".format(i), mo)
               for i, mo in enumerate(mos_slice, 1)]

    # Reconstruct .molden-file
    joined_mos = "\n".join(occ_mos)
    new_molden = header + "[MO]\n" + joined_mos
    return new_molden


def parse_molden_mos(text):
    """Expects everything after the [MO] tag of a .molden file."""
    int_ = pp.Word(pp.nums).setParseAction(
                                lambda s, loc, toks: int(toks[0])
    )
    float_ = pp.Word(pp.nums + ".-").setParseAction(
                                        lambda s, loc, toks: float(toks[0])
    )
    ene = pp.Literal("Ene=") + float_.setResultsName("energy")
    a_or_b = pp.Or(pp.Literal("Alpha").setResultsName("spin"),
                   pp.Literal("Beta").setResultsName("spin"))
    spin = pp.Literal("Spin=") + a_or_b
    occup = pp.Literal("Occup=") + float_.setResultsName("occup")
    ao_line = pp.Suppress(int_) + float_
    molecular_orbital = pp.Group(ene
                                 + spin
                                 + occup
                                 + pp.OneOrMore(ao_line).setResultsName("coeffs"))

    parser = pp.OneOrMore(molecular_orbital)
    mos = parser.parseString(text)
    #mo0 = mos[0]
    #print(mo0.energy)
    #print(mo0.spin)
    #print(mo0.occup)
    #print(mo0.coeffs)
    #print(len(mo0.coeffs))
    return mos


def join_parsed_mo(mo):
    ao_line_strs = [f"{i: 5d} {coeff: 16.10f}" for i, coeff in enumerate(mo.coeffs, 1)]
    ao_str = "\n ".join(ao_line_strs)
    return f"""Ene=\t{mo.energy}
    Spin= {mo.spin}
    Occup= {mo.occup}
    {ao_str}"""


if __name__ == "__main__":
    fn = "/home/carpx/Dokumente/projekte/runobpb/runobpb/mspt2_vtzp_3states/runotz.rasscf.1.molden"
    with open(fn) as handle:
        text = handle.read()
    as_ = get_jmol_active_space(text)
    for l in as_:
        print(l)
