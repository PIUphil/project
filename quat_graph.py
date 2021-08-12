import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 4*np.pi, 3600)
plt.xticks(np.arange(0, 4.2*np.pi, np.pi), labels=['0', 'π', '2π','3π','4π'])
plt.yticks(np.arange(-1, 1.2, 1))
plt.grid(True, axis='x', color='gray', alpha=0.5, linestyle='--')
plt.grid(True, axis='y', color='gray', alpha=0.5, linestyle='--')
plt.plot(x, np.cos(0.5*x), color='#6DAEE2', label='Quat[0]')
plt.plot(x, np.sin(0.5*x), color='#EA96A3', label='Quat[3]')
plt.legend()
plt.show()
