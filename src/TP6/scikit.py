from scipy import misc
import matplotlib.pyplot as plt

f = misc.imread("cat.jpg")
r = misc.imresize(f, 0.1)

# plt.imshow(f)
plt.imshow(r)
plt.show()
