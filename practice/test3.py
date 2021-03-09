import matplotlib.pyplot as plt
import numpy as np
import math

x = np.arange(0.0, 5.0, 0.01)
y1 = [math.sin(i) for i in x]
y2 = [math.sin(i*2)*3 for i in x]

plt.plot(x, y1, 'r', label = "y=sin(x)")
plt.plot(x, y2, 'b' , label = "y=3sin(2x)")

plt.legend()
plt.grid(True)
plt.show()