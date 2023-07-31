# 随机梯度下降的逻辑分类

import matplotlib.pyplot as plt
import numpy as np

train = np.loadtxt('files/data2.csv', delimiter=',', skiprows=1)
train_x = train[:, 0:2]
train_y = train[:, 2]

theta = np.random.rand(4)

mu = train_x.mean(axis=0)
sigma = train_x.std(axis=0)


def standardize(x):
    return (x - mu) / sigma


train_z = standardize(train_x)


def to_matrix(x):
    x0 = np.ones([x.shape[0], 1])
    x3 = x[:, 0, np.newaxis] ** 2
    return np.hstack([x0, x, x3])


X = to_matrix(train_z)


def f(x):
    return 1 / (1 + np.exp(-np.dot(x, theta)))


ETA = 1e-3
epoch = 5000
for _ in range(epoch):
    p = np.random.permutation(X.shape[0])
    for x, y in zip(X[p, :], train_y[p]):
        theta = theta - ETA * (f(x) - y) * x

x0 = np.linspace(-2, 2, 100)

plt.plot(train_z[train_y == 1, 0], train_z[train_y == 1, 1], 'o')
plt.plot(train_z[train_y == 0, 0], train_z[train_y == 0, 1], 'x')
plt.plot(x0, -(theta[0] + theta[1] * x0 + theta[3] * x0 ** 2) / theta[2], linestyle='dashed')
plt.show()
