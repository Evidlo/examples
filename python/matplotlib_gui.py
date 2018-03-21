#!/bin/env python3
# Evan Widloski - 2018-03-21
# Interactive experiment with covariance matrices
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

# define slider positions (axes)
slide_x2_axis = plt.axes([0.25, 0.05, 0.65, 0.03])
slide_x12_axis = plt.axes([0.25, 0.1, 0.65, 0.03])
slide_x1_axis = plt.axes([0.25, 0.15, 0.65, 0.03])
slide_samples_axis = plt.axes([0.25, 0.2, 0.65, 0.03])

# define sliders
slide_x1 = Slider(slide_x1_axis, '$\sigma_1^2$', 0, 10, valinit=1)
slide_x12 = Slider(slide_x12_axis, '$\sigma_{12}$', 0, 10, valinit=2)
slide_x2 = Slider(slide_x2_axis, '$\sigma_2^2$', 0, 10, valinit=4)
slide_samples = Slider(slide_samples_axis, 'Samples', 1, 1000, valinit=100)

# initialize empty plot
plt.subplots_adjust(left=0.1, bottom=0.3)
plt.subplot(1,1,1)
p, = plt.plot(np.empty(0), 'o')
plt.axis([-10, 10, -10, 10])
plt.grid('on')
plt.title('Covariance interactive Applet')

# callback function when sliders are changed
def update(_):
    x1 = slide_x1.val
    x12 = slide_x12.val
    x2 = slide_x2.val
    samples = int(slide_samples.val)
    cov_mat = np.matrix([[x1, x12], [x12, x2]])
    pop_mean = [0, 0]
    x = np.random.multivariate_normal(pop_mean, cov_mat, samples)
    p.set_xdata(x[:, 0])
    p.set_ydata(x[:, 1])
    plt.show()

slide_x1.on_changed(update)
slide_x12.on_changed(update)
slide_x2.on_changed(update)
slide_samples.on_changed(update)

# initialize plot at startup
update(None)

plt.show()
