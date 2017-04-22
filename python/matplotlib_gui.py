#!/bin/python
# Evan Widloski - 2016-10-13
# Visually demonstrate f(z) = e^z
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3)

a = 1
b = 0
c = 0
t = np.arange(-5, 5, 0.001)
line = a*(t - c) + b

plt.subplot(1,2,1)
l, = plt.plot(t, line, lw=2, color='red')
plt.title('$z$ plane')
plt.axis([-10, 10, -10, 10])
plt.subplot(1,2,2)
plt.title('$e^z$ plane')
l2, = plt.plot(t, line, lw=2, color='red')
plt.axis([-10, 10, -10, 10])


axis_color = 'lightgoldenrodyellow'
slide_a_axis = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axis_color)
slide_b_axis = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axis_color)
slide_c_axis = plt.axes([0.25, 0.2, 0.65, 0.03], axisbg=axis_color)

slide_a = Slider(slide_a_axis, 'Slope', -30, 30, valinit=a)
slide_b = Slider(slide_b_axis, 'Shift Imaginary', -10, 10, valinit=b)
slide_c = Slider(slide_c_axis, 'Shift Real', -10, 10, valinit=c)


def update(val):
    a = slide_a.val
    b = slide_b.val
    c = slide_c.val
    t = np.arange(-5 + c, 5 + c, 0.001)
    l.set_xdata(t)
    l.set_ydata(a*(t - c) + b)
    # import pdb
    # pdb.set_trace()
    ez = np.power(np.e,np.vectorize(complex)(t,a*(t - c) + b))
    l2.set_xdata(np.real(ez))
    l2.set_ydata(np.imag(ez))
    fig.canvas.draw_idle()

slide_a.on_changed(update)
slide_b.on_changed(update)
slide_c.on_changed(update)

reset_axes = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(reset_axes, 'Reset', color=axis_color, hovercolor='0.975')


def reset(event):
    slide_a.reset()
    slide_b.reset()
    slide_c.reset()
button.on_clicked(reset)

update(0)

plt.show()
