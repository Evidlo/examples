from keras.models import Sequential
from keras.layers import Dense
from matplotlib import pyplot as plt
import numpy as np

from sklearn.datasets import make_moons
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split

A, B = make_moons(noise=0.2, random_state=0, n_samples=1000)
A = scale(A)

A_train, A_test, B_train, B_test = train_test_split(A, B, test_size=.3)


model = Sequential()
model.add(Dense(32, input_dim=2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(
    optimizer='AdaDelta',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.fit(
    A_train, B_train, batch_size=32, epochs=200,
    verbose=0, validation_data=(A_test, B_test)
)

# x = np.linspace(-3, 3, 100)
# xx, yy = np.meshgrid(x, x)
# grid = n
# prediction_probs = model.predict_proba()


grid = np.mgrid[-3:3:100j,-3:3:100j]
grid_2d = grid.reshape(2, -1).T
A, B = grid
plt.hold(True)
prediction_probs = model.predict_proba(grid_2d, batch_size=32, verbose=0)
contour = plt.contourf(A, B, prediction_probs.reshape(100, 100))
plt.scatter(A_test[B_test==0, 0], A_test[B_test==0, 1], color='b', label='A')
plt.scatter(A_test[B_test==1, 0], A_test[B_test==1, 1], color='r', label='B')

plt.show()
plt.legend()
