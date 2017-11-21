#!/usr/bin/env python3

import numpy as np

from qchelper.conversion import invcm2eV

class Parser:

    def __init__(self, fn, parser):
        self.fn = fn
        self.parser = parser(self.fn)

        self.data = self.parser.parse()
        self._text = None

    @property
    def text(self):
        if self._text is None:
            with open(self.fn) as handle:
                self._text = handle.read()
        return self._text

    def parse_ets(self):
        """Parse ground and excited state energies using cclib.

        This neglects any disperion correction used in the calculation!

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

        scf_energy = self.data.scfenergies
        assert(len(scf_energy) == 1)
        et_energies = self.data.etenergies
        et_energies = invcm2eV(d.etenergies)
        # Add the ground state energy to the array
        all_energies = np.full(et_energies.size + 1, scf_energy)
        all_energies[1:] += et_energies
        return all_energies

    @property
    def imgvibfreqs(self):
        vibfreqs = self.data.vibfreqs
        return vibfreqs[np.where(vibfreqs < 0)]

    def __str__(self):
        return self.fn
