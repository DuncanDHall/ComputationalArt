import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import curves


fig = plt.figure(figsize=[1,1])
ax = fig.add_subplot(111)

path = Path(*curves.compound1())
patch = patches.PathPatch(path, facecolor='none', lw=1)
ax.add_patch(patch)

ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.1)

plt.axis('off')
plt.savefig("test.svg")
