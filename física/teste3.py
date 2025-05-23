import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# Função potencial
def potential(x, y, z):
    r_pos = np.sqrt(x ** 2 + y ** 2 + (z - d / 2) ** 2)
    r_neg = np.sqrt(x ** 2 + y ** 2 + (z + d / 2) ** 2)
    return k * q * (1 / r_pos - 1 / r_neg)

fig = plt.figure(figsize=(14, 6))
ax = fig.add_subplot(111, projection='3d')

# Malha 3D mais densa para suavização
x = np.linspace(-1, 1, 50)
y = np.linspace(-1, 1, 50)
z = np.linspace(0.1, 1, 50)
X, Y, Z = np.meshgrid(x, y, z)
phi = potential(X, Y, Z)

# Slider para corte dinâmico
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
slider = Slider(ax_slider, 'Corte em Z', 0.1, 1, valinit=0.5)


def update(val):
    z_cut = slider.val
    idx = np.argmin(np.abs(z - z_cut))
    ax.clear()

    # Superfície equipotencial
    ax.contourf(X[:, :, idx], Y[:, :, idx], phi[:, :, idx],
                levels=20, cmap='viridis', zdir='z', offset=z_cut)

    # Linhas de campo no plano
    Ex = -(potential(X[:, :, idx] + h, Y[:, :, idx], z_cut) - potential(X[:, :, idx] - h, Y[:, :, idx], z_cut)) / (
                2 * h)
    Ey = -(potential(X[:, :, idx], Y[:, :, idx] + h, z_cut) - potential(X[:, :, idx], Y[:, :, idx] - h, z_cut)) / (
                2 * h)
    ax.streamplot(X[:, :, idx], Y[:, :, idx], Ex, Ey, color='w', linewidth=0.7, density=2)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(0, 1)
    ax.set_title(f'Mapa de Potencial com Corte em z = {z_cut:.2f}')


slider.on_changed(update)
update(0.5)
plt.tight_layout()
plt.show()