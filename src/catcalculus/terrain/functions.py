import numpy as np
from typing import Callable

# Tipo para funciones de terreno
TerrainFunction = Callable[[np.ndarray, np.ndarray], np.ndarray]


def meadow(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Prado suave:
        f(x, y) = 0.2 * (x^2 + y^2)
    """
    return 0.2 * (x**2 + y**2)


def wavy_mountain(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Montaña ondulada:
        f(x, y) = sin(x) * cos(y)
    """
    return np.sin(x) * np.cos(y)


def meow_volcano(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Volcán con cráter ancho y borde elevado.
    """
    r = np.sqrt(x**2 + y**2)

    crater = -np.exp(-(r**2) * 3)
    ring = np.exp(-(r - 2)**2) * 2
    slope = -0.1 * r

    return crater + ring + slope



def infinite_peak(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Pico infinito:
        f(x, y) = ln(x^2 + y^2 + 1)
    """
    r2 = x**2 + y**2
    peak = 3 * np.exp(-0.5 * r2)
    shoulders = 0.5 * np.exp(-0.1 * r2)
    return peak + shoulders

