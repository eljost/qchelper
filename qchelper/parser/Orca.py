#!/usr/bin/env python3

import re

from cclib.parser import ORCA
import numpy as np

from qchelper.conversion import invcm2eV, au2eV
from qchelper.parser.Parser import Parser

class Orca(Parser):

    def __init__(self, fn):
        super().__init__(fn, parser=ORCA)

    def parse_scf_e(self):
        scf_energy_re = "FINAL SINGLE POINT ENERGY\s*([-\.\d]+)"
        scf_energy = float(re.search(scf_energy_re, self.text).groups()[0])
        return au2eV(scf_energy)

    def parse_actual_ets(self):
        """Parse ground and excited state energies using cclib.

        This includes any dispersion correction used in the calculation.

        Parameters
        ----------
        fn : str
             .log file to be parsed.
        parser : str
                 Class name of a cclib parser.

        Returns
        -------
        all_energies : np.array
                       Shape (Number of electronic states, ). Total energies
                       of the electronic states.
        """

        scf_energy = self.parse_scf_e()

        et_energies = self.data.etenergies
        et_energies = invcm2eV(self.data.etenergies)
        # Add the ground state energy to the array
        all_energies = np.full(et_energies.size + 1, scf_energy)
        all_energies[1:] += et_energies
        return all_energies

    def parse_mayer(self):
        mayer_re = "Mayer bond orders larger than 0.1\s*(.+?)\n\n"
        matches = re.search(mayer_re, self.text, re.DOTALL)
        #print(matches.groups()[0].split())
        #matches = [m.strip() for m in matches.groups()[1split(":")
        
        return matches

    def parse_tddft_table(self):
        transition_dipole_re = "TRANSITION ELECTRIC.+?TZ(.+?)\n\n"
        mobj = re.search(transition_dipole_re, self.text, re.DOTALL)
        table_lines = mobj.groups()[0].split("\n")[3:]
        return [l.split() for l in table_lines]
