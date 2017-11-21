#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from natsort import natsorted
import orbkit as ok

ITYPES = {
    ".fchk": "gaussian.fchk",
    ".out": "gaussian.log",
    ".log": "gaussian.log",
}


def orbkit_can_parse(path):
    """Checks a path for files that can be parsed by orbkit and returns
    them as a list."""

    fns = list()
    abs_fns = list()
    for fn in os.listdir(path):
        ext = os.path.splitext(fn)[1]
        if ext in ITYPES:
            abspath = os.path.abspath(os.path.join(path, fn))
            fns.append(fn)
            abs_fns.append(abspath)
    fns = natsorted(fns)
    abs_fns = natsorted(abs_fns)
    return fns, abs_fns


def orbkit_read(fn):
    """Read a file with orbkit. The itype is determined from the file
    extension."""

    ext = os.path.splitext(fn)[1]
    itype = ITYPES[ext]
    return ok.read.main_read(fn, itype=itype, all_mo=True)


def orbkit_loader(path):
    """Scan a directory for files that can be parsed by orbkit and return
    them as a list of QCinfo objects and a list containing the filenames."""

    fns, abs_fns = orbkit_can_parse(path)
    qcinfos = [orbkit_read(abs_fn) for abs_fn in abs_fns]
    return qcinfos, fns


def fchk_to_qcinfo(fn):
    """Read a gaussian fchk file with orbkit and return a QCinfo object."""


def glog_to_qcinfo(fn):
    """Read a gaussian log file with orbkit and return a QCinfo object."""
    return ok.read.main_read(fn, itype="gaussian.log", all_mo=True)
