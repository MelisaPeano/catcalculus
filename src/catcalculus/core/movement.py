import numpy as np

def terrain_gradient(Z):
    """
    Devuelve los gradientes gx, gy del terreno Z.
    """
    gx, gy = np.gradient(Z)
    return gx, gy


def _world_to_grid(cat, terrain):
    """
    Convierte coordenadas (x,y) del gato al índice más cercano en la grilla del terreno.
    """
    x_vals = terrain.x[0]        # columnas
    y_vals = terrain.y[:, 0]     # filas

    i = (np.abs(y_vals - cat.y)).argmin()
    j = (np.abs(x_vals - cat.x)).argmin()

    return i, j


def move_cat_by_gradient(cat, terrain, step=0.05, uphill=False):
    """
    Mueve al gato siguiendo el gradiente del terreno:
    - uphill = True → hacia arriba (subida)
    - uphill = False → hacia abajo (bajada)
    """
    gx, gy = terrain_gradient(terrain.z)

    i, j = _world_to_grid(cat, terrain)

    dx = gx[i, j]
    dy = gy[i, j]

    # Dirección
    if not uphill:
        dx, dy = -dx, -dy

    # Normalizar
    mag = np.sqrt(dx*dx + dy*dy)
    if mag > 0:
        dx /= mag
        dy /= mag

    # Escalar por agilidad del gato
    dx *= step * cat.agility
    dy *= step * cat.agility

    cat.move(dx, dy)
