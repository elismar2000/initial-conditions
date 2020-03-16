import numpy as np
import matplotlib.pyplot as plt

n = 2000
y = np.vstack((np.random.sample(n) * 2, np.random.sample(n)))
x = np.zeros(n)

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
ax1.plot(y[0], y[1], x, '.', zdir='z')

y = np.vstack((y[0], y[1], x))

theta = -np.pi / 3
phi = np.pi / 6

Rx = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
Rz = np.array([[np.cos(phi), -np.sin(phi), 0], [np.sin(phi), np.cos(phi), 0], [0, 0, 1]])

y = np.matmul(Rz, y)
y = np.matmul(Rx, y)

ax1.plot(y[0], y[1], y[2], '.', zdir='z')
ax1.set_aspect('equal')
plt.show()
