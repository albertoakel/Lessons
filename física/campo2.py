import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def electric_field_dipole(x, y, z, p_magnitude=1.0):
    """
    Calcula o campo elétrico de um dipolo elétrico vertical (momento p na direção z)
    em coordenadas cartesianas.
    Considera o centro do dipolo na origem (0,0,0).
    Args:
        x, y, z (np.array): Coordenadas dos pontos onde o campo será calculado.
        p_magnitude (float): Magnitude do momento de dipolo.
    Returns:
        tuple: (Ex, Ey, Ez, E_magnitude)
    """
    # Vetor momento de dipolo (vertical, ao longo do eixo z)
    p = np.array([0, 0, p_magnitude])

    # Vetor posição r: Combine x, y, z em uma única array com a dimensão do vetor no final
    # A forma (X, Y, Z) é (num_x, num_y, num_z) para cada coordenada.
    # Precisamos de r_vec como (num_x, num_y, num_z, 3) para facilitar as operações.
    r_vec = np.stack((x, y, z), axis=-1) # Isso cria um array (..., 3)

    # Magnitude de r
    r_magnitude = np.linalg.norm(r_vec, axis=-1) # Norma ao longo da última dimensão (o vetor 3D)

    # Evita divisão por zero no centro do dipolo
    r_magnitude[r_magnitude == 0] = np.finfo(float).eps

    # Vetor unitário r_hat
    r_hat = r_vec / r_magnitude[..., np.newaxis] # Expande r_magnitude para broadcast correto

    # Produto escalar (p . r_hat) para cada ponto.
    # np.einsum 'i, ...i -> ...' faz o produto escalar do vetor 'p' (índice i)
    # com a última dimensão de 'r_hat' (também índice i), somando sobre 'i',
    # e mantendo as outras dimensões de 'r_hat'.
    p_dot_r_hat = np.einsum('i, ...i -> ...', p, r_hat)

    # Cálculo do campo elétrico E = (1/4πε₀) * (1/r³) * [3(p·r̂)r̂ - p]
    # Considerando 1/4πε₀ = 1 para simplificar

    # term1: 3 * (p.r_hat) * r_hat
    # p_dot_r_hat é agora uma array com a mesma forma de X, Y, Z.
    # Precisamos expandi-la para que possa ser multiplicada por r_hat (que tem a dimensão do vetor no final)
    term1 = 3 * p_dot_r_hat[..., np.newaxis] * r_hat

    # term2: p (vetor momento de dipolo)
    # Precisamos que 'p' tenha a mesma forma para subtração que 'term1',
    # ou que o broadcasting funcione corretamente.
    # 'p' já é (3,). Quando subtraído de 'term1' (..., 3), o broadcasting funciona.
    # Não é mais necessário p[:, np.newaxis] se r_hat for (..., 3)

    E_x = (1 / r_magnitude**3) * (term1[..., 0] - p[0])
    E_y = (1 / r_magnitude**3) * (term1[..., 1] - p[1])
    E_z = (1 / r_magnitude**3) * (term1[..., 2] - p[2])

    E_magnitude = np.sqrt(E_x**2 + E_y**2 + E_z**2)

    return E_x, E_y, E_z, E_magnitude

# --- Configurações da malha ---
# Definir o intervalo para x, y, z. Considerar z >= 0 para semi-espaço.
x_range = np.linspace(-0.5, 0.5, 15) # 15 pontos para melhor visualização
y_range = np.linspace(-0.5, 0.5, 15)
z_range = np.linspace(0.01, 0.5, 10) # z ligeiramente acima de 0 para evitar singularidade e considerar semi-espaço

# Criar a malha de pontos
X, Y, Z = np.meshgrid(x_range, y_range, z_range, indexing='ij') # Use 'ij' para que X,Y,Z tenham shape (len(x), len(y), len(z))

# Calcular o campo elétrico em cada ponto da malha
Ex, Ey, Ez, E_magnitude = electric_field_dipole(X, Y, Z)

# --- Plotagem 3D ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Quiver plot (vetores do campo)
# Reduzir a densidade para uma visualização mais clara em 3D
ax.quiver(X[::2, ::2, ::2], Y[::2, ::2, ::2], Z[::2, ::2, ::2],
          Ex[::2, ::2, ::2], Ey[::2, ::2, ::2], Ez[::2, ::2, ::2],
          length=0.05, normalize=True, color='blue', alpha=0.7)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Campo Elétrico de um Dipolo Vertical (3D)')
ax.scatter(0, 0, 0, color='red', marker='o', s=100, label='Centro do Dipolo')
ax.legend()
plt.tight_layout()
plt.show()


# --- Visualização nos 3 planos (XY, XZ, YZ) e Isolinhas ---

# --- Plano XY (z constante) ---
# Escolher um valor de z para o plano XY (o mais próximo de 0.01 ou um valor pequeno)
z_plane_xy = z_range[0] # Ou outro valor representativo
X_xy, Y_xy = np.meshgrid(x_range, y_range, indexing='ij') # Usar 'ij' consistente
# Certificar que Z_xy tem a mesma forma para o full_like
Ex_xy, Ey_xy, Ez_xy, E_magnitude_xy = electric_field_dipole(X_xy, Y_xy, np.full_like(X_xy, z_plane_xy))

fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Plotagem do Campo Elétrico no Plano XY
ax0 = axs[0]
ax0.streamplot(X_xy, Y_xy, Ex_xy, Ey_xy, color=E_magnitude_xy, cmap='viridis', density=2)
# Isolinhas da magnitude do campo no Plano XY
# Use E_magnitude_xy.min() e .max() para os níveis, garantindo que não sejam zero
min_val = np.min(E_magnitude_xy[E_magnitude_xy > 0]) # Evitar log de zero
max_val = np.max(E_magnitude_xy)
if min_val > 0 and max_val > min_val: # Apenas se houver uma variação válida
    contour_xy = ax0.contour(X_xy, Y_xy, E_magnitude_xy, levels=np.logspace(np.log10(min_val), np.log10(max_val), 10), cmap='plasma')
    fig.colorbar(contour_xy, ax=ax0, label='Magnitude do Campo E')
else:
    print(f"Aviso: Não foi possível plotar isolinhas no plano XY. Min/Max Magnitude: {min_val}/{max_val}")

ax0.scatter(0, 0, color='red', marker='o', s=100, label='Centro do Dipolo')
ax0.set_xlabel('X')
ax0.set_ylabel('Y')
ax0.set_title(f'Campo E e Isolinhas (Plano XY, z={z_plane_xy:.2f})')
ax0.set_aspect('equal', adjustable='box') # Garante proporção igual entre os eixos
ax0.legend()

# --- Plano XZ (y constante) ---
# Escolher um valor de y para o plano XZ
y_plane_xz = y_range[len(y_range)//2] # y = 0
X_xz, Z_xz = np.meshgrid(x_range, z_range, indexing='ij') # Usar 'ij' consistente
Ex_xz, Ey_xz, Ez_xz, E_magnitude_xz = electric_field_dipole(X_xz, np.full_like(X_xz, y_plane_xz), Z_xz)

ax1 = axs[1]
ax1.streamplot(X_xz, Z_xz, Ex_xz, Ez_xz, color=E_magnitude_xz, cmap='viridis', density=2)
# Isolinhas da magnitude do campo no Plano XZ
min_val = np.min(E_magnitude_xz[E_magnitude_xz > 0])
max_val = np.max(E_magnitude_xz)
if min_val > 0 and max_val > min_val:
    contour_xz = ax1.contour(X_xz, Z_xz, E_magnitude_xz, levels=np.logspace(np.log10(min_val), np.log10(max_val), 10), cmap='plasma')
    fig.colorbar(contour_xz, ax=ax1, label='Magnitude do Campo E')
else:
    print(f"Aviso: Não foi possível plotar isolinhas no plano XZ. Min/Max Magnitude: {min_val}/{max_val}")

ax1.scatter(0, 0, color='red', marker='o', s=100, label='Centro do Dipolo')
ax1.set_xlabel('X')
ax1.set_ylabel('Z')
ax1.set_title(f'Campo E e Isolinhas (Plano XZ, y={y_plane_xz:.2f})')
ax1.set_aspect('equal', adjustable='box')
ax1.legend()


# --- Plano YZ (x constante) ---
# Escolher um valor de x para o plano YZ
x_plane_yz = x_range[len(x_range)//2] # x = 0
Y_yz, Z_yz = np.meshgrid(y_range, z_range, indexing='ij') # Usar 'ij' consistente
Ex_yz, Ey_yz, Ez_yz, E_magnitude_yz = electric_field_dipole(np.full_like(Y_yz, x_plane_yz), Y_yz, Z_yz)

ax2 = axs[2]
ax2.streamplot(Y_yz, Z_yz, Ey_yz, Ez_yz, color=E_magnitude_yz, cmap='viridis', density=2)
# Isolinhas da magnitude do campo no Plano YZ
min_val = np.min(E_magnitude_yz[E_magnitude_yz > 0])
max_val = np.max(E_magnitude_yz)
if min_val > 0 and max_val > min_val:
    contour_yz = ax2.contour(Y_yz, Z_yz, E_magnitude_yz, levels=np.logspace(np.log10(min_val), np.log10(max_val), 10), cmap='plasma')
    fig.colorbar(contour_yz, ax=ax2, label='Magnitude do Campo E')
else:
    print(f"Aviso: Não foi possível plotar isolinhas no plano YZ. Min/Max Magnitude: {min_val}/{max_val}")

ax2.scatter(0, 0, color='red', marker='o', s=100, label='Centro do Dipolo')
ax2.set_xlabel('Y')
ax2.set_ylabel('Z')
ax2.set_title(f'Campo E e Isolinhas (Plano YZ, x={x_plane_yz:.2f})')
ax2.set_aspect('equal', adjustable='box')
ax2.legend()


plt.tight_layout()
plt.show()