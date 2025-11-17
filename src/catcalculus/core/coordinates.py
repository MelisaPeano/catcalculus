from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class WorldBounds:
    """
    Define los límites del mundo continuo en el plano XY.

    Ejemplo: x ∈ [-3, 3], y ∈ [-3, 3]
    """
    x_min: float
    x_max: float
    y_min: float
    y_max: float

    def width(self) -> float:
        return self.x_max - self.x_min

    def height(self) -> float:
        return self.y_max - self.y_min


@dataclass
class CoordinateSystem:
    """
    Sistema de coordenadas que sabe convertir entre:

    - Mundo continuo (x, y)
    - Grilla discreta (i, j) de tamaño (rows, cols)

    rows = cantidad de puntos en eje y
    cols = cantidad de puntos en eje x
    """
    world_bounds: WorldBounds
    grid_shape: Tuple[int, int]  # (rows, cols)

    @property
    def rows(self) -> int:
        return self.grid_shape[0]

    @property
    def cols(self) -> int:
        return self.grid_shape[1]

    def clamp_world(self, x: float, y: float) -> Tuple[float, float]:
        """
        Recorta (x, y) para que siempre caiga dentro de los límites del mundo.
        """
        xb = self.world_bounds
        x_clamped = min(max(x, xb.x_min), xb.x_max)
        y_clamped = min(max(y, xb.y_min), xb.y_max)
        return x_clamped, y_clamped

    def world_to_grid(self, x: float, y: float) -> Tuple[int, int]:
        """
        Convierte (x, y) continuos a índices de grilla (i, j).

        i -> índice de fila (eje y)
        j -> índice de columna (eje x)
        """
        x, y = self.clamp_world(x, y)
        xb = self.world_bounds

        # Normalizar a [0, 1]
        nx = (x - xb.x_min) / xb.width()
        ny = (y - xb.y_min) / xb.height()

        # Escalar a índices de 0 a N-1
        j = int(round(nx * (self.cols - 1)))
        i = int(round(ny * (self.rows - 1)))

        # Seguridad por si round se pasa un poquito
        i = max(0, min(self.rows - 1, i))
        j = max(0, min(self.cols - 1, j))
        return i, j

    def grid_to_world(self, i: int, j: int) -> Tuple[float, float]:
        """
        Convierte índices de grilla (i, j) a coordenadas continuas (x, y)
        apuntando aproximadamente al centro de la celda.
        """
        i = max(0, min(self.rows - 1, i))
        j = max(0, min(self.cols - 1, j))

        xb = self.world_bounds

        nx = j / max(1, (self.cols - 1))
        ny = i / max(1, (self.rows - 1))

        x = xb.x_min + nx * xb.width()
        y = xb.y_min + ny * xb.height()

        return x, y
