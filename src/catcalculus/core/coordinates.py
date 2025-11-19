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
    Sistema que convierte entre:

    - Mundo continuo (x, y)
    - Grilla discreta (i, j) de tamaño (rows, cols)

    rows = cantidad de puntos en eje y
    cols = cantidad de puntos en eje x
    """
    world_bounds: WorldBounds
    grid_shape: Tuple[int, int]  # (rows, cols)

    def __post_init__(self) -> None:
        # filas y columnas
        self.rows: int = self.grid_shape[0]
        self.cols: int = self.grid_shape[1]

        # Tamaño de cada celda en el mundo continuo
        self.dx: float = self.world_bounds.width() / max(1, (self.cols - 1))
        self.dy: float = self.world_bounds.height() / max(1, (self.rows - 1))

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

        # Clamp por seguridad
        i = max(0, min(self.rows - 1, i))
        j = max(0, min(self.cols - 1, j))
        return i, j

    def grid_to_world(self, i: int, j: int) -> Tuple[float, float]:
        """
        Convierte índices de grilla (i, j) a coordenadas continuas (x, y),
        apuntando al centro aproximado de la celda.
        """
        i = max(0, min(self.rows - 1, i))
        j = max(0, min(self.cols - 1, j))

        xb = self.world_bounds

        x = xb.x_min + j * self.dx
        y = xb.y_min + i * self.dy

        return x, y
