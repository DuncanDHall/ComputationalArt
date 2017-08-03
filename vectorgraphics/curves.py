import matplotlib.pyplot as plt
from matplotlib.path import Path

def curve1():

    verts = [
        (0., 0.),  # P0
        (0.2, 1.), # P1
        (1., 0.8), # P2
        (0.8, 0.), # P3
    ]

    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4
    ]

    return verts, codes


def compound1():

    verts = [
        # first sub curve
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, 1.0),
        (0.5, 0.5),
        # second sub curve
        (0.5, 0.0),
        (1.0, 0.0),
        (1.0, 0.5),
    ]

    codes = [
        # first sub curve
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        # second sub curve
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    return verts, codes


def compound2():

    verts = [
        # first sub curve
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, 0.5),
        # second sub curve
        (1.0, 0.0),
        (1.0, 0.5),
    ]

    codes = [
        # first sub curve
        Path.MOVETO,
        Path.CURVE3,
        Path.CURVE3,
        # second sub curve
        Path.CURVE3,
        Path.CURVE3,
    ]

    return verts, codes


def gen_compound(num_curves):
    # generates a compound set of 3 point curves which each share a
    # tangent at their terminus with the next.
    # arguments:
    #   num_curves - int number of sub curves
    pass

    verts = np.random.rand(1, num_curves * 2 + 1)
    codes = [Path.MOVETO]














