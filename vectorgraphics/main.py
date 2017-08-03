import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.path import Path
from tqdm import tqdm

import curves
import mandala

def plot_points(ax, verts):
    ax.plot(verts[:,0], verts[:,1], 'x', lw=1, color='red', ms=10)


def plot_curve(ax, verts, codes):
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', lw=1)
    ax.add_patch(patch)


def make_figs(num):

    for n in tqdm(range(num)):
        fig = plt.figure(figsize=[6,10])
        ax = fig.add_subplot(111)

        verts, codes = curves.gen_compound1(3)
        plot_curve(ax, verts, codes)
        # plot_points(ax, verts)

        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.5, 1.5)

        plt.axis('off')
        plt.savefig("out/curve{}.svg".format(n))
        plt.close()


def make_mandalas(num):

    for n in tqdm(range(num)):
        fig = plt.figure(figsize=[10,10])
        ax = fig.add_subplot(111)

        verts0, codes = curves.gen_compound1(5)
        vertss = mandala.mandalate(verts0)
        for verts in vertss:
            plot_curve(ax, verts, codes)
        # plot_points(ax, verts)

        ax.set_xlim(-2.0, 2.0)
        ax.set_ylim(-2.0, 2.0)

        plt.axis('off')
        plt.savefig("out/mandala{}.svg".format(n))
        plt.close()


if __name__ == "__main__":
    make_mandalas(40)
