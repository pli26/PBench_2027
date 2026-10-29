import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle

# Hatch style
mpl.rcParams['hatch.color'] = 'black'
mpl.rcParams['hatch.linewidth'] = 1.5

fig, ax = plt.subplots(figsize=(4, 2))

rect = Rectangle(
    (0.1, 0.1),      # (x, y)
    0.8,             # width
    0.5,             # height
    facecolor='skyblue',
    edgecolor='black',
    linewidth = 0,
    hatch='//',
)

ax.add_patch(rect)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.show()
