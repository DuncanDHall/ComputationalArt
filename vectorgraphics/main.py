import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import curves
from tqdm import tqdm


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


if __name__ == "__main__":
    make_figs(40)
