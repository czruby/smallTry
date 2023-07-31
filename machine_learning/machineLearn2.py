# 多重回归
import matplotlib.pyplot as plt
import numpy as np

train = np.loadtxt('files/data.csv', delimiter=',', skiprows=1)
train_x = train[:, 0]
train_y = train[:, 1]

theta = np.random.rand(3)


# 预测函数
def f(x):
    return np.dot(x, theta)


def MSE(x, y):
    return (1 / x.shape[0]) * np.sum((y - f(x)) ** 2)


def to_matrix(x):
    return np.vstack([np.ones(x.shape[0]), x, x ** 2]).T


mu = train_x.mean()
sigma = train_x.std()


def standardize(x):
    return (x - mu) / sigma


train_z = standardize(train_x)
X = to_matrix(train_z)

ETA = 1e-3
diff = 1
errors = []
errors.append(MSE(X, train_y))
while diff > 1e-2:
    theta = theta - ETA * np.dot(f(X) - train_y, X)
    errors.append(MSE(X, train_y))
    diff = errors[-2] - errors[-1]

x = np.linspace(-2, 2, 100)
plt.plot(train_z, train_y, 'o')
plt.plot(x, f(to_matrix(x)))
plt.show()

y = np.arange(len(errors))
plt.plot(y, errors)
plt.show()
