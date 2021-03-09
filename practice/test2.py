import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0.0, 5.0, 0.01)

plt.title('my graph')
plt.plot(x, x, 'g', label="y=x")
plt.plot(x, 2*(x+1), 'r', label='y=2*(x+1)')

plt.xlabel('X DAta')
plt.xlabel('Y DAta')

plt.legend()

plt.grid(True)
plt.show()