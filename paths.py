#!/usr/bin/env python3

import itertools
import os
import re


def search_recursivly(top, fn_re):
    """Search recursivly for files that match a supplied regex.

    Parameters
    ----------
    top : str
        Path to the root dir from where the search starts.
    fn_re : str
        Valid regular expression that matches the wanted filenames.

    Returns
    -------
    full_paths : list
        Full paths to the matched filenames.
    """

    full_paths = list()
    for root, dirs, files in os.walk(top):
        matched = [fn for fn in files if re.match(fn_re, fn)]
        full_paths.extend([os.path.join(root, fn) for fn in matched])
    return full_paths


def search_files_with_ext(top, ext=".out", ignore_fns=[]):
    """Search recursivly for files with a certain extensions with the ability
    to ignore some of them.

    Parameters
    ----------
    top : str
        Path to the root dir from where the search starts.
    ext : str, optional
        File extension to search for.
    ignore_fns : iterable of str, optional
        Ignore found files if they contain a string from this iterable.

    Returns
    -------
    full_paths : list
        Full paths to the found files.
    """

    full_paths = list()
    for root, dirs, files in os.walk(top):
        ext_fns = [fn for fn in files if fn.endswith(ext)]
        full_paths.extend([os.path.join(root, ext_fn) for ext_fn in ext_fns])

    if ignore_fns:
        return [full_path for full_path, ignore_fn
                in itertools.product(full_paths, ignore_fns)
                if ignore_fn not in full_path
        ]

    return full_paths
