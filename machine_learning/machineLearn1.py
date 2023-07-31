# 回归
import matplotlib.pyplot as plt
import numpy as np

train = np.loadtxt('files/data.csv', delimiter=',', skiprows=1)
train_x = train[:, 0]
train_y = train[:, 1]

theta0 = np.random.rand()
theta1 = np.random.rand()


# 预测函数
def f(x):
    return theta0 + theta1 * x


# 目标函数
def E(x, y):
    return 0.5 * np.sum((y - f(x)) ** 2)


mu = train_x.mean()
sigma = train_x.std()


def standardize(x):
    return (x - mu) / sigma


train_z = standardize(train_x)

ETA = 1e-3
diff = 1
count = 0
error = E(train_z, train_y)
while diff > 1e-2:
    tmp0 = theta0 - ETA * np.sum((f(train_z) - train_y))
    tmp1 = theta1 - ETA * np.sum((f(train_z) - train_y) * train_z)
    theta0 = tmp0
    theta1 = tmp1
    current_error = E(train_z, train_y)
    diff = error - current_error
    error = current_error
    count += 1
    log = ' 第 {} 次 : theta0 = {:.3f}, theta1 = {:.3f}, 差值 = {:.4f}'
    print(log.format(count, theta0, theta1, diff))

x = np.linspace(-2, 2, 100)
plt.plot(train_z, train_y, 'o')
plt.plot(x, f(x))
plt.show()
