import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

# Parâmetros do dipolo
q = 1e-9  # Carga (C)
d = 0.2  # Distância entre as cargas (m)
k = 8.99e9  # Constante eletrostática (N·m²/C²)

# Criação da malha 2D para os plots (evitando z=0)
x = np.linspace(-1, 1, 20)
y = np.linspace(-1, 1, 20)
z = np.linspace(0.1, 1, 10)  # Evita divisão por zero


# Função potencial
def potential(x, y, z):
    r_pos = np.sqrt(x ** 2 + y ** 2 + (z - d / 2) ** 2)
    r_neg = np.sqrt(x ** 2 + y ** 2 + (z + d / 2) ** 2)
    return k * q * (1 / r_pos - 1 / r_neg)


# Configuração da figura
fig = plt.figure(figsize=(15, 8))
ax_3d = fig.add_subplot(121, projection='3d')
ax_2d = fig.add_subplot(122)


# Função para atualizar a visualização
def update_plot(plane):
    ax_3d.clear()
    ax_2d.clear()

    if plane == 'XY':
        z_slice = 0.5
        X_plane, Y_plane = np.meshgrid(x, y)
        Z_plane = np.full_like(X_plane, z_slice)

        # Potencial e campo
        phi = potential(X_plane, Y_plane, z_slice)
        h = 1e-6
        Ex = -(potential(X_plane + h, Y_plane, z_slice) - potential(X_plane - h, Y_plane, z_slice)) / (2 * h)
        Ey = -(potential(X_plane, Y_plane + h, z_slice) - potential(X_plane, Y_plane - h, z_slice)) / (2 * h)
        E_norm = np.sqrt(Ex ** 2 + Ey ** 2)
        Ex, Ey = Ex / E_norm, Ey / E_norm

        # Plot 3D
        ax_3d.quiver(X_plane, Y_plane, Z_plane, Ex, Ey, np.zeros_like(Ex),
                     length=0.1, color='r')
        ax_3d.set_title(f'Vetores do Campo (Plano XY, z = {z_slice})')

        # Plot 2D
        contour = ax_2d.contour(X_plane, Y_plane, phi, levels=15, cmap='viridis')
        ax_2d.streamplot(X_plane, Y_plane, Ex, Ey, color='k', density=1.5)
        ax_2d.set_title(f'Isolinhas e Linhas de Campo (XY)')

    elif plane == 'XZ':
        y_slice = 0.0
        X_plane, Z_plane = np.meshgrid(x, z)
        Y_plane = np.full_like(X_plane, y_slice)

        # Potencial e campo
        phi = potential(X_plane, y_slice, Z_plane)
        h = 1e-6
        Ex = -(potential(X_plane + h, y_slice, Z_plane) - potential(X_plane - h, y_slice, Z_plane)) / (2 * h)
        Ez = -(potential(X_plane, y_slice, Z_plane + h) - potential(X_plane, y_slice, Z_plane - h)) / (2 * h)
        E_norm = np.sqrt(Ex ** 2 + Ez ** 2)
        Ex, Ez = Ex / E_norm, Ez / E_norm

        # Plot 3D
        ax_3d.quiver(X_plane, Y_plane, Z_plane, Ex, np.zeros_like(Ex), Ez,
                     length=0.1, color='b')
        ax_3d.set_title(f'Vetores do Campo (Plano XZ, y = {y_slice})')

        # Plot 2D
        contour = ax_2d.contour(X_plane, Z_plane, phi, levels=15, cmap='viridis')
        ax_2d.streamplot(X_plane, Z_plane, Ex, Ez, color='k', density=1.5)
        ax_2d.scatter(0, d / 2, color='red', s=100, label='+q')
        ax_2d.scatter(0, -d / 2, color='blue', s=100, label='-q')
        ax_2d.set_title(f'Isolinhas e Linhas de Campo (XZ)')
        ax_2d.legend()

    elif plane == 'YZ':
        x_slice = 0.0
        Y_plane, Z_plane = np.meshgrid(y, z)
        X_plane = np.full_like(Y_plane, x_slice)

        # Potencial e campo
        phi = potential(x_slice, Y_plane, Z_plane)
        h = 1e-6
        Ey = -(potential(x_slice, Y_plane + h, Z_plane) - potential(x_slice, Y_plane - h, Z_plane)) / (2 * h)
        Ez = -(potential(x_slice, Y_plane, Z_plane + h) - potential(x_slice, Y_plane, Z_plane - h)) / (2 * h)
        E_norm = np.sqrt(Ey ** 2 + Ez ** 2)
        Ey, Ez = Ey / E_norm, Ez / E_norm

        # Plot 3D
        ax_3d.quiver(X_plane, Y_plane, Z_plane, np.zeros_like(Ey), Ey, Ez,
                     length=0.1, color='g')
        ax_3d.set_title(f'Vetores do Campo (Plano YZ, x = {x_slice})')

        # Plot 2D
        contour = ax_2d.contour(Y_plane, Z_plane, phi, levels=15, cmap='viridis')
        ax_2d.streamplot(Y_plane, Z_plane, Ey, Ez, color='k', density=1.5)
        ax_2d.scatter(0, d / 2, color='red', s=100, label='+q')
        ax_2d.scatter(0, -d / 2, color='blue', s=100, label='-q')
        ax_2d.set_title(f'Isolinhas e Linhas de Campo (YZ)')
        ax_2d.legend()

    # Configurações comuns
    ax_3d.set_xlabel('X')
    ax_3d.set_ylabel('Y')
    ax_3d.set_zlabel('Z')
    ax_3d.set_xlim(-1, 1)
    ax_3d.set_ylim(-1, 1)
    ax_3d.set_zlim(0, 1)

    ax_2d.set_aspect('equal')
    ax_2d.set_xlabel('X' if plane != 'YZ' else 'Y')
    ax_2d.set_ylabel('Z' if plane != 'XY' else 'Y')
    plt.colorbar(contour, ax=ax_2d, label='Potencial (V)')
    plt.tight_layout()


# Botões de rádio
rax = plt.axes([0.02, 0.4, 0.1, 0.15])
radio = RadioButtons(rax, ('XY', 'XZ', 'YZ'))
radio.on_clicked(update_plot)

# Visualização inicial
update_plot('XZ')
plt.show()
