import numpy as np
from catcalculus.cats.models import Cat
from .coordinates import CoordinateSystem

def terrain_gradient(Z: np.ndarray):
    """
    Devuelve los gradientes gx, gy del terreno Z.
    """
    # Usamos np.gradient sobre el array de altitud Z
    gy, gx = np.gradient(Z)
    return gx, gy


def _world_to_grid(cat: Cat, terrain: object) -> tuple[int, int]:
    """
    Convierte coordenadas (x,y) del gato al índice más cercano en la grilla del terreno.
    """
    x_vals = terrain.x[0]        # columnas (eje x)
    y_vals = terrain.y[:, 0]     # filas (eje y)

    j = np.argmin(np.abs(x_vals - cat.x))
    i = np.argmin(np.abs(y_vals - cat.y))

    # Aseguramos que los índices estén dentro de los límites
    i = max(0, min(terrain.z.shape[0] - 1, i))
    j = max(0, min(terrain.z.shape[1] - 1, j))

    return i, j


def move_cat_by_gradient(cat: Cat, terrain: object, coord_sys: CoordinateSystem, step_factor: float = 0.5, uphill: bool = False) -> float | None:
    """
    Mueve al gato siguiendo el gradiente del terreno.
    Retorna la magnitud del gradiente en el punto actual, o None si no hay movimiento posible.
    """
    gx, gy = terrain_gradient(terrain.z)

    i, j = _world_to_grid(cat, terrain)

    # Las componentes del vector gradiente en el punto del gato
    dx = gx[i, j]
    dy = gy[i, j]

    mag = np.sqrt(dx*dx + dy*dy)

    # Si la magnitud es cero o muy pequeña, no se mueve
    if mag == 0:
        return 0.0

    # Dirección: gradiente descendente (bajada) o ascendente (subida)
    if not uphill:
        dx, dy = -dx, -dy

    # Normalizar el vector de dirección
    dx /= mag
    dy /= mag

    # Factor del paso dependiente de la magnitud y agilidad
    effective_step = mag * step_factor * cat.agility

    # Escalar por el tamaño del paso
    final_dx = dx * effective_step
    final_dy = dy * effective_step

    # 1. Calcular la nueva posición potencial
    new_x = cat.x + final_dx
    new_y = cat.y + final_dy

    # 2. Restringir la posición a los límites del mundo (CLAMPING)
    clamped_x, clamped_y = coord_sys.clamp_world(new_x, new_y)

    # 3. Calcular el movimiento EFECTIVO (diferencia entre el punto restringido y el actual)
    effective_dx = clamped_x - cat.x
    effective_dy = clamped_y - cat.y

    # 4. Aplicar el movimiento
    cat.move(effective_dx, effective_dy)

    # Retornamos la magnitud del gradiente para que el motor decida si el gato se detiene
    return mag