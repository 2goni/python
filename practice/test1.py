import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0.0, 5.0, 0.01)

plt.subplot(221)
plt.plot(x, x**2, 'r--')

plt.subplot(222)
plt.plot(x, 3**x, 'b')

plt.subplot(223)
plt.plot(x, x, 'g-')

plt.subplot(224)
plt.plot(x, 1/(x+1), 'y')

plt.show()
