# 正则化验证
import numpy as np
import matplotlib.pyplot as plt
import standardize


def g(x):
    return 0.1 * (x ** 3 + x ** 2 + x)


train_x = np.linspace(-2, 2, 8)
train_y = g(train_x) + np.random.randn(train_x.size) * 0.05

x = np.linspace(-2, 2, 100)


def to_matrix(x):
    return np.vstack([
        np.ones(x.size),
        x,
        x ** 2,
        x ** 3,
        x ** 4,
        x ** 5,
        x ** 6,
        x ** 7,
        x ** 8,
        x ** 9,
        x ** 10,
    ]).T


train_z = standardize.Standardize(train_x).standardize()
X = to_matrix(train_z)


def f(x):
    return np.dot(x, theta)


# 不用正则化
theta = np.random.randn(X.shape[1])


def E(x, y):
    return 0.5 * np.sum((y - f(x)) ** 2)


ETA = 1e-4
diff = 1
error = E(X, train_y)
while diff > 1e-6:
    theta = theta - ETA * np.dot(f(X) - train_y, X)
    current_error = E(X, train_y)
    diff = error - current_error
    error = current_error

z = standardize.Standardize(x).standardize()

plt.plot(train_z, train_y, 'o')
plt.plot(z, f(to_matrix(z)), linestyle='dashed')

# 使用正则化
theta = np.random.randn(X.shape[1])

ETA = 1e-4
LAMDA = 1
diff = 1
error = E(X, train_y)
while diff > 1e-6:
    reg_term = LAMDA * np.hstack([0, theta[1:]])
    theta = theta - ETA * (np.dot(f(X) - train_y, X) + reg_term)
    current_error = E(X, train_y)
    diff = error - current_error
    error = current_error
z = standardize.Standardize(x).standardize()
plt.plot(z, f(to_matrix(z)))
plt.ylim(-1, 2)
plt.show()
