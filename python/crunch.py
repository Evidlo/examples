import numpy as np
import matplotlib.pyplot as plt

dat = open('Logo.bam', 'rb').read()
dat = np.array([int(b) for b in dat])

# allow for 30 byte header/footer
widths = [x for x in range(300, 800) if len(dat) % x < 30]

dat = dat[10:]
# for width in widths:
while True:
# for width in range(500, 800):
    height = int(input('height:'))
    trimmed_data = dat[len(dat) % height:]
    width = len(trimmed_data) // height
    print(height)
    plt.imshow(trimmed_data.reshape((width, height)))
    plt.pause(.3)
    plt.cla()
