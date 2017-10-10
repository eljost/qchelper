import pathlib

import simplejson as json

def orientation_menu(orients_dict):
    as_list = [(mol, orients_dict[mol]) for mol in orients_dict]
    valid_selections = range(len(as_list))

    print("Available orientations:")
    for i, (molecule, _) in enumerate(as_list):
        print("\t{:>3}: {:>15}".format(i, molecule))
    selection = input("Please select a molecule ({}-{}): ".format(
                                                        min(valid_selections),
                                                        max(valid_selections))
    )
    try:
        selection = int(selection)
    except ValueError:
        logging.warning("Please enter an integer!")
        return orientation_menu(orients_dict)
    if selection not in valid_selections:
        logging.warning("Invalid selection!")
        return orientation_menu(orients_dict)
    return as_list[selection][1]


def load_orientations(orientations_fn=".orientations.json"):
    """Look for orientations in $HOME/.orientations.json"""
    home = pathlib.Path.home()
    orientations_fn = home / orientations_fn
    with open(orientations_fn) as handle:
        orients_dict = json.load(handle)
    return orients_dict
