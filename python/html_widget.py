from ipywidgets.interact import static_widget_script
from ipywidgets import StaticInteract, RangeWidget
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import face


def plot(noise_snr):
    f = face(gray=True)
    fig, ax = plt.subplots()
    ax.imshow(f + np.random.normal(size=f.shape, scale=noise_snr))
    return fig

static = StaticInteract(plot, noise_snr=RangeWidget(0, 10, 1))
open('/tmp/test.html', 'w').write(
    '<!DOCTYPE html>\n<html\n' + static.html() + static_widget_script + '</html>'
)
