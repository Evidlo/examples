#!/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.lines as lines

fig = plt.figure()
ax = fig.add_subplot(111)

# l1 = lines.Line2D([0, 1], [0, 1], transform=fig.transFigure, figure=fig)
# l2 = lines.Line2D([0, 1], [1, 0], transform=fig.transFigure, figure=fig)
l1 = lines.Line2D([0, 1], [0, 1], transform=fig.transFigure, figure=fig)
l2 = lines.Line2D([0, 1], [1, 0], transform=fig.transFigure, figure=fig)

fig.lines.extend([l1, l2])

plt.show()
