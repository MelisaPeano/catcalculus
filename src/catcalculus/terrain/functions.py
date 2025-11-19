import numpy as np
from typing import Callable

# Tipo para funciones de terreno: recibe (x, y) y devuelve z
TerrainFunction = Callable[[np.ndarray, np.ndarray], np.ndarray]


def meadow(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Prado suave: superficie convexa y tranquila.

        f(x, y) = 0.2 * (x^2 + y^2)
    """
    return 0.2 * (x**2 + y**2)


def wavy_mountain(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Montaña ondulada: crestas periódicas en X e Y.

        f(x, y) = sin(x) * cos(y)
    """
    return np.sin(x) * np.cos(y)


def meow_volcano(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Volcán con cráter ancho y borde elevado.

    - Centro hundido (cráter)
    - Anillo elevado alrededor
    - Pendiente suave hacia afuera
    """
    r = np.sqrt(x**2 + y**2)

    crater = -np.exp(-(r**2) * 3)        # pozo central
    ring = 2 * np.exp(-(r - 2)**2)       # anillo elevado cerca de r ≈ 2
    slope = -0.1 * r                     # cae suavemente lejos del volcán

    return crater + ring + slope


def infinite_peak(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Pico alto y muy concentrado en el centro, con base suave alrededor.
    """
    r2 = x**2 + y**2
    peak = 3 * np.exp(-0.5 * r2)         # pico muy alto en el centro
    shoulders = 0.5 * np.exp(-0.1 * r2)  # base más ancha y suave
    return peak + shoulders
