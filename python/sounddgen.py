import sounddevice as sd
import numpy as np
from numpy import sin

def square(t):
    return 2.0 * (t % (2 * np.pi) < np.pi) - 1

fs = 44100
duration = 10

t = np.linspace(0, duration, duration * fs)
l = np.sin(2 * np.pi * 1000 * t)
r = np.sin(2 * np.pi * 1000 * t + (np.pi / 2))

r = np.sin(2 * np.pi * 1000 * t)
l = square(2 * np.pi * 1000 * t + (np.pi / 2))

x = np.vstack((l, r))

sd.play(x.T, fs)
