import brewer2mpl
import numpy as np
from scipy.optimize import minimize_scalar

params = {
    "text.usetex" : True,
    "text.latex.preamble" : "\\usepackage{siunitx}",
    "font.family" : "serif",
    "font.size" : 16,
    "font.serif" : ['computer modern roman'],
}
lsize = 10
colors = brewer2mpl.get_map("Set1", "qualitative", 8).mpl_colors


def diff(arr1, arr2, x):
    """Return the difference between two vectors where one vector
    is shifted by x."""
    return np.sum(arr1 - arr2 + x)**2


def space_vals(this_val, next_val, min_off):
    """Assure that the two supplied values lie at least
    'min_off' apart."""
    if next_val < this_val:
        return this_val + min_off
    diff = abs(next_val - this_val)
    if diff < min_off:
        next_val += min_off - diff
    return next_val


def recalc_vert_spacing(ax, xs, ys, size):
    """Assure that the supplied ys don't overlap."""
    t = lambda xy: ax.transData.transform(xy)
    ti = lambda xy: ax.transData.inverted().transform(xy)
    # Transform to display coordinates 
    xy_displ = np.array([t(xy) for xy in zip(xs, ys)])
    # Minimum offset between labels in y-direction
    min_off = size * 1.25
    for i, (x, y) in enumerate(xy_displ[:-1]):
        next_y = xy_displ[i+1,1]
        xy_displ[i+1,1] = space_vals(y, next_y, min_off)

    ys_spaced = np.array(ti(xy_displ))[:,1]
    d = lambda x: diff(ys, ys_spaced, x)
    res = minimize_scalar(d)
    return ys_spaced - res.x


def plot_labels(ax, xs, ys, labels, thresh=0.1, size=lsize):
    new_ys = recalc_vert_spacing(ax, xs, ys, size)
    for i, (x, y) in enumerate(zip(xs, new_ys)):
        ax.text(x, y, labels[i], va="center", size=size)


def annotate_transition(osc, trans, ax):
    if type(trans) is type(list()):
        index, trans_str = trans
        trans_str  = "${}$".format(trans_str)
    else:
        index = trans
        trans_str = "$S_{{{}}}$".format(trans)
    # Because the array index starts at 0 and not at 1
    index = (index - 1) * 3 + 1
    xy = osc[index]
    x, y  = xy
    x += .05
    y += 0.0125
    ax.annotate(trans_str, xy=xy, xytext=(x, y),backgroundcolor="w",size=14)
