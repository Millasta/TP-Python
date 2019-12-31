import numpy as np
from random import randrange
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import misc

# EX1
print("1.")
a = np.zeros((4, 3, 2))
with np.nditer(a, op_flags=['readwrite']) as it:
    for x in it:
        x[...] = randrange(-100, 100, 1)
print(a)
print("ndim : " + str(a.ndim))
print("shape : " + str(a.shape))
print("size : " + str(a.size))
print("dtype : " + str(a.dtype))
print("itemsize : " + str(a.itemsize))
print("data : " + str(a.data))

#EX2
print("2.")
mat1 = np.zeros((3, 3))
with np.nditer(mat1, op_flags=['readwrite']) as it:
    for x in it:
        x[...] = randrange(0, 9, 1)

mat2 = np.zeros((3, 3))
with np.nditer(mat2, op_flags=['readwrite']) as it:
    for x in it:
        x[...] = randrange(2, 11, 1)
print(mat2)

prod1 = mat1 * mat2
print(prod1)

prod2 = mat1.dot(mat2)
print(prod1)

trans = mat1.transpose()
print(trans)

#EX3
print("3.")
sys = np.array( [ [2., 1.5, 1],
                  [.5, 1., 3.],
                  [2., 3., .25] ] )
sys2 = np.array( [-1., 4., 3.] )

print(np.linalg.det(sys))
print(np.linalg.inv(sys))
print(np.linalg.solve(sys, sys2))
print(np.linalg.eig(sys))

#EX4
print("4.")
def func(x, a, b, c):
    return a * np.exp(-b * x) + c

xdata = np.linspace(0, 4, 50)
y = func(xdata, 2.5, 1.3, 0.5)
y_noise = 0.1 * np.random.normal(size=xdata.size)
ydata = y + y_noise
plt.plot(xdata, ydata, 'b-', label='data')

popt, pcov = curve_fit(func, xdata, ydata)
plt.plot(xdata, func(xdata, *popt), 'r-')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

#EX5
print("5.")
f = misc.imread("cat.jpg")
r = misc.imresize(f, 0.1)

# plt.imshow(f)
plt.imshow(r)
plt.show()

