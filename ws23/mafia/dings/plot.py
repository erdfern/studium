import numpy as np
import matplotlib.pyplot as plt

n = 4
z_k_4 = [np.cos(2 * np.pi * k / n) + 1j * np.sin(2 * np.pi * k / n) for k in range(n)]

x_coords = [np.real(z) for z in z_k_4]
y_coords = [np.imag(z) for z in z_k_4]

theta = np.linspace(0, 2*np.pi, 100)
plt.figure(figsize=(6,6))
plt.plot(np.cos(theta), np.sin(theta), label="Einheitskreis $K$")
plt.scatter(x_coords, y_coords, color='red')
plt.grid(True)
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.title("Punkte $z_{k,4}$ auf dem Einheitskreis")
plt.xlabel("Realteil")
plt.ylabel("Imaginärteil")
plt.axis('equal')

for i, (x, y) in enumerate(zip(x_coords, y_coords)):
    plt.text(x, y, f'  $z_{{ {i},4 }}$', verticalalignment='bottom', horizontalalignment='right')

plt.show()